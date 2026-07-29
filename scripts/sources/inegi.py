"""Conector INEGI (BIE). Requiere INEGI_TOKEN.

Consulta la API de Indicadores del INEGI (Banco de Información Económica, BIE)
para las series cuyo ID esté confirmado en config/series.json. Cada indicador
con `serie` no nula se descarga y se devuelve como una ACTUALIZACIÓN DE COLUMNA
(no como un indicador completo): el pipeline la fusiona sobre la columna objetivo
del indicador existente, conservando el resto de columnas/desgloses de respaldo.

Prueba controlada V1: solo IGAE total (clave 737121, base BIE-BISE, geografía
nacional 00) tiene su ID confirmado; el resto de los indicadores del INEGI
conservan `serie: null` y se omiten (se mantiene el dato de respaldo). Cuando
falta el token o no hay IDs confirmados, devuelve SourceResult(ok=False) y el
pipeline conserva los datos previos.
"""
from __future__ import annotations

import os

from .base import SourceResult, http_get_json

ENDPOINT = ("https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
            "INDICATOR/{ids}/es/{geo}/false/{db}/2.0/{token}?type=json")

DEFAULT_DB = "BIE-BISE"
DEFAULT_GEO = "00"

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
_MES_IDX = {m: i + 1 for i, m in enumerate(MESES)}


def ym_to_label(ym: str) -> str:
    """Convierte 'AAAA-MM' a la etiqueta del tablero ('May 26')."""
    year, month = ym.split("-")
    mi = int(month)
    return f"{MESES[mi - 1]} {year[-2:]}"


def label_to_ym(period: str) -> str | None:
    """Convierte una etiqueta mensual del tablero ('Abr 26 P') a 'AAAA-MM'.

    Devuelve None si la etiqueta no es mensual (p. ej. trimestrales '1T-25').
    """
    parts = (period or "").split()
    if len(parts) < 2:
        return None
    mi = _MES_IDX.get(parts[0][:3].capitalize())
    if mi is None:
        return None
    try:
        yy = int(parts[1])
    except ValueError:
        return None
    return f"{2000 + yy:04d}-{mi:02d}"


def _tp_to_ym(time_period: str) -> str | None:
    """Convierte 'AAAA/MM' del BIE a 'AAAA-MM'."""
    tp = (time_period or "").strip()
    if "/" not in tp:
        return None
    y, m = tp.split("/", 1)
    try:
        mi = int(m)
    except ValueError:
        return None
    if not (1 <= mi <= 12) or len(y) != 4 or not y.isdigit():
        return None
    return f"{y}-{mi:02d}"


def _parse_series(raw: dict) -> tuple[list[dict], dict] | None:
    """Extrae observaciones mensuales ordenadas y metadatos de la serie."""
    series = (raw or {}).get("Series") or []
    if not series:
        return None
    s = series[0]
    meta = {
        "indicador": s.get("INDICADOR"),
        "freq": s.get("FREQ"),
        "unit": s.get("UNIT"),
        "lastupdate": s.get("LASTUPDATE"),
        "source": s.get("SOURCE"),
    }
    obs = []
    for o in s.get("OBSERVATIONS") or []:
        ym = _tp_to_ym(o.get("TIME_PERIOD"))
        val = o.get("OBS_VALUE")
        if ym is None or val in (None, ""):
            continue
        try:
            num = float(val)
        except (TypeError, ValueError):
            continue
        obs.append({"ym": ym, "value": num})
    obs.sort(key=lambda x: x["ym"])
    return obs, meta


def fetch(config: dict, start_year: int = 2018) -> SourceResult:
    token = os.environ.get("INEGI_TOKEN")
    if not token:
        return SourceResult(False, warnings=[
            "INEGI_TOKEN ausente: se omite la actualización desde INEGI; se conservan datos previos."])
    inegi = config.get("inegi", {})
    confirmed = {k: v for k, v in inegi.items()
                 if isinstance(v, dict) and v.get("serie")}
    if not confirmed:
        return SourceResult(False, warnings=[
            "INEGI: no hay IDs de serie confirmados en config/series.json. "
            "Confírmalos contra el catálogo del BIE antes de activar la descarga; "
            "se conservan los datos previos."])

    data: dict = {}
    warnings: list[str] = []
    for key, spec in confirmed.items():
        serie_id = str(spec["serie"])
        url = ENDPOINT.format(ids=serie_id, token=token,
                              db=spec.get("db", DEFAULT_DB),
                              geo=spec.get("geo", DEFAULT_GEO))
        try:
            raw = http_get_json(url)
        except Exception as e:  # noqa: BLE001 - resiliencia del pipeline
            warnings.append(f"INEGI {key}: error de consulta (serie {serie_id}): {e}")
            continue
        parsed = _parse_series(raw)
        if not parsed or not parsed[0]:
            warnings.append(f"INEGI {key}: respuesta sin observaciones (serie {serie_id}).")
            continue
        obs, meta = parsed
        obs = [o for o in obs if int(o["ym"][:4]) >= start_year]
        if not obs:
            warnings.append(f"INEGI {key}: sin observaciones desde {start_year} (serie {serie_id}).")
            continue

        last = obs[-1]
        data[key] = {
            "target_column": int(spec.get("columna_objetivo", 0)),
            "api_total": obs,
            "serie": serie_id,
            "link": spec.get("link"),
            "api_meta": {
                "serie": serie_id, "freq": meta.get("freq"), "unit": meta.get("unit"),
                "lastupdate": meta.get("lastupdate"), "n_obs": len(obs),
                "ultimo_valor": round(last["value"], 6),
                "ultima_ym": last["ym"], "ultima_observacion": ym_to_label(last["ym"]),
            },
        }
        warnings.append(
            f"INEGI {key}: {len(obs)} observaciones (serie {serie_id}, base "
            f"{spec.get('db', DEFAULT_DB)}); última {ym_to_label(last['ym'])} = "
            f"{round(last['value'], 6)}; actualización BIE {meta.get('lastupdate')}.")

    return SourceResult(bool(data), data=data, warnings=warnings)
