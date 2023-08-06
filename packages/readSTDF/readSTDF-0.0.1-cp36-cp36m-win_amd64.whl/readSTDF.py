from datetime import datetime
from pathlib import Path
from _readSTDF import _readSTDF


__all__ = ['readSTDF']


def readSTDF(file_name, record_type: str, n: int = 1):
    """Read and parse STDF records.

    Args:
        file_name: path of STDF file, can be a `str` or `Path`.
        record_type: STDF Record Types, FAR, ATR, MIR, etc.
        n: max number of results, default n = 1, set n = -1 for all results.

    Returns:
        A list for record results. Each result is a dict mapping fields to value.
        For Example, for record_type=FAR, the results could be [{'CPU_TYPE': 1, 'STDF_VER': 4}].

    Raises:
        TypeError: An error occurred when file_name is not a `str` or `Path`.
        IOError: An error occurred when file_name is not a file.
    """

    if isinstance(file_name, str):
        path = Path(file_name)
    elif isinstance(file_name, Path):
        path = file_name
        file_name = str(file_name)
    else:
        raise TypeError('Argument \'file_name\' should be `str` or `Path`!')
    if not path.is_file():
        raise IOError(f'{file_name} is not a file!')
    record_type = record_type.upper()
    record = _readSTDF(file_name, record_type, n)
    return _parse(record, record_type)


def _parse(record, record_type):
    parse_map = {
        'FAR': _parseFAR,
        'ATR': _parseATR,
        'MIR': _parseMIR,
        'MRR': _parseMRR,
        'PCR': _parsePCR,
        'HBR': _parseHBR,
        'SBR': _parseSBR,
        'PMR': _parsePMR,
        'PGR': _parsePGR,
        'PLR': _parsePLR,
        'RDR': _parseRDR,
        'SDR': _parseSDR,
        'WIR': _parseWIR,
        'WRR': _parseWRR,
        'WCR': _parseWCR,
        'PIR': _parsePIR,
        'PRR': _parsePRR,
        'TSR': _parseTSR,
        'PTR': _parsePTR,
        'MPR': _parseMPR,
        'FTR': _parseFTR,
        'BPS': _parseBPS,
        'EPS': _parseEPS,
        'GDR': _parseGDR,
        'DTR': _parseDTR,
    }
    return [parse_map[record_type](r) for r in record]


def _parseFAR(record):
    return record


def _parseATR(record):
    _parseTime(record, ['MOD_TIM'])
    _parseCn(record, ['CMD_LINE'])
    return record


def _parseMIR(record):
    _parseTime(record, ['SETUP_T', 'START_T'])
    _parseC1(record, ['MODE_COD', 'RTST_COD', 'PROT_COD', 'CMOD_COD'])
    _parseCn(record, ['LOT_ID', 'PART_TYP', 'NODE_NAM', 'TSTR_TYP', 'JOB_NAM', 'JOB_REV', 'SBLOT_ID', 'OPER_NAM', 'EXEC_TYP', 'EXEC_VER', 'TEST_COD', 'TST_TEMP', 'USER_TXT', 'AUX_FILE', 'PKG_TYP', 'FAMILY_ID', 'DATE_COD', 'FACIL_ID', 'FLOOR_ID', 'PROC_ID', 'OPER_FRQ', 'SPEC_NAM', 'SPEC_VER', 'FLOW_ID', 'SETUP_ID', 'DSGN_REV', 'ENG_ID', 'ROM_COD', 'SERL_NUM', 'SUPR_NAM'])
    return record


def _parseMRR(record):
    _parseTime(record, ['FINISH_T'])
    _parseC1(record, ['DISP_COD'])
    _parseCn(record, ['USR_DESC', 'EXC_DESC'])
    return record


def _parsePCR(record):
    return record


def _parseHBR(record):
    _parseC1(record, ['HBIN_PF'])
    _parseCn(record, ['HBIN_NAM'])
    return record


def _parseSBR(record):
    _parseC1(record, ['SBIN_PF'])
    _parseCn(record, ['SBIN_NAM'])
    return record


def _parsePMR(record):
    _parseCn(record, ['CHAN_NAM', 'PHY_NAM'])
    return record


def _parsePGR(record):
    _parseCn(record, ['GRP_NAM'])
    return record


def _parsePLR(record):
    _parsexU1(record, ['GRP_RADX'])
    return record


def _parseRDR(record):
    return record


def _parseSDR(record):
    _parsexU1(record, ['SITE_NUM'])
    _parseCn(record, ['HAND_TYP', 'HAND_ID', 'CARD_TYP', 'CARD_ID', 'LOAD_TYP', 'LOAD_ID', 'DIB_TYP', 'DIB_ID', 'CABL_TYP', 'CABL_ID', 'CONT_TYP', 'CONT_ID', 'LASR_TYP', 'LASR_ID', 'EXTR_TYP', 'EXTR_ID'])
    return record


def _parseWIR(record):
    _parseTime(record, ['START_T'])
    _parseCn(record, ['WAFER_ID'])
    return record


def _parseWRR(record):
    _parseTime(record, ['FINISH_T'])
    _parseCn(record, ['WAFER_ID', 'FABWF_ID', 'FRAME_ID', 'MASK_ID', 'USR_DESC', 'EXC_DESC'])
    return record


def _parseWCR(record):
    return record


def _parsePIR(record):
    return record


def _parsePRR(record):
    _parseCn(record, ['PART_ID', 'PART_TXT'])
    _parseB1(record, ['PART_FLG'])
    _parseBn(record, ['PART_FIX'])
    return record


def _parseTSR(record):
    _parseC1(record, ['TEST_TYP'])
    _parseB1(record, ['OPT_FLAG'])
    _parseCn(record, ['TEST_NAM', 'SEQ_NAME', 'TEST_LBL'])
    return record


def _parsePTR(record):
    _parseB1(record, ['TEST_FLG', 'PARM_FLG', 'OPT_FLAG'])
    _parseCn(record, ['TEST_TXT', 'ALARM_ID', 'UNITS', 'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT'])
    return record


def _parseMPR(record):
    _parseB1(record, ['TEST_FLG', 'PARM_FLG', 'OPT_FLAG'])
    _parseCn(record, ['TEST_TXT', 'ALARM_ID', 'UNITS', 'UNITS_IN', 'C_RESFMT', 'C_LLMFMT', 'C_HLMFMT'])
    return record


def _parseFTR(record):
    _parseB1(record, ['TEST_FLG', 'OPT_FLAG'])
    _parseCn(record, ['VECT_NAM', 'TIME_SET', 'OP_CODE', 'TEST_TXT', 'ALARM_ID', 'PROG_TXT', 'RSLT_TXT'])
    return record


def _parseBPS(record):
    _parseCn(record, ['SEQ_NAME'])
    return record


def _parseEPS(record):
    return record


def _parseGDR(record):
    return record


def _parseDTR(record):
    _parseCn(record, ['TEXT_DAT'])
    return record


def _parseTime(record, fields):
    for f in fields:
        record[f] = datetime.fromtimestamp(record[f])


def _parseC1(record, fields):
    for f in fields:
        record[f] = chr(record[f])


def _parseCn(record, fields):
    for f in fields:
        record[f] = record[f][1:]
        try:
            record[f] = record[f].decode()
        except UnicodeDecodeError:
            pass


def _parseB1(record, fields):
    for f in fields:
        record[f] = bin(record[f])


def _parseBn(record, fields):
    for f in fields:
        if record[f]:
            record[f] = [bin(record[f][i]) if i < len(record[f]) else '0b0' for i in range(1, record[f][0] + 1)]
        else:
            record[f] = ''


def _parsexU1(record, fields):
    for f in fields:
        record[f] = [i for i in record[f]]
