"""Utilitários para manipulação de data e hora."""
from datetime import datetime, timezone, timedelta
from typing import Optional

# Timezone do Brasil (UTC-3)
BR_TIMEZONE = timezone(timedelta(hours=-3))


def now_br() -> datetime:
    """Retorna a data/hora atual no timezone do Brasil (UTC-3)."""
    return datetime.now(BR_TIMEZONE)


def now_utc() -> datetime:
    """Retorna a data/hora atual em UTC."""
    return datetime.now(timezone.utc)


def to_br_timezone(dt: datetime) -> datetime:
    """Converte um datetime para o timezone do Brasil."""
    if dt.tzinfo is None:
        # Assume que é UTC se não tem timezone
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(BR_TIMEZONE)


def to_utc_timezone(dt: datetime) -> datetime:
    """Converte um datetime para UTC."""
    if dt.tzinfo is None:
        # Assume que é BR se não tem timezone
        dt = dt.replace(tzinfo=BR_TIMEZONE)
    return dt.astimezone(timezone.utc)


def format_br_datetime(dt: Optional[datetime] = None) -> str:
    """Formata datetime no padrão brasileiro (DD/MM/AAAA HH:MM:SS)."""
    if dt is None:
        dt = now_br()
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=BR_TIMEZONE)
    else:
        dt = dt.astimezone(BR_TIMEZONE)
    
    return dt.strftime("%d/%m/%Y %H:%M:%S")