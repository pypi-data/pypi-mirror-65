import warnings
import aghplctools.ingestion.csv
import aghplctools.ingestion.text


# passthrough definitions with warnings to support legacy calls
# todo wait a few versions and remove these definitions
def pull_hplc_area_from_csv(folder, report_name='Report'):
    warnings.warn(
        f'The pull_hplc_area_from_csv has been refactored into aghplctools.ingestion.csv '
        f'Please change your import statements',
        DeprecationWarning,
        stacklevel=2,
    )
    return aghplctools.ingestion.csv.pull_hplc_area_from_csv(
        folder,
        report_name,
    )


def pull_metadata_from_csv(folder, report_name='Report'):
    warnings.warn(
        f'The pull_metadata_from_csv has been refactored into aghplctools.ingestion.csv '
        f'Please change your import statements',
        DeprecationWarning,
        stacklevel=2,
    )
    return aghplctools.ingestion.csv.pull_metadata_from_csv(
        folder,
        report_name,
    )


def pull_hplc_area_from_txt(filename):
    warnings.warn(
        f'The pull_hplc_area_from_txt has been refactored into aghplctools.ingestion.text '
        f'Please change your import statements',
        DeprecationWarning,
        stacklevel=2,
    )
    return aghplctools.ingestion.text.pull_hplc_area_from_txt(
        filename
    )
