import logging 
from database import DatabaseManager
from ingest_data import DataIngest
from check_data import data_view

def run_main():
    logging.basicConfig(
        filename='master.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True
    )
    logger = logging.getLogger("Master")
    logger.info("Starting")

    try:
        db_manager = DatabaseManager()
        db_manager.init_db()

        ingest = DataIngest(folder_name='data', file_name='hr_analytics.csv')
        ingest.run_ingestion()

        view=data_view()
        view.display_records(limit=5)

        logging.info("Run Successfully.")

    except Exception as e:
        logging.error(f"Run crashed: {e}")

if __name__=="__main__":
    run_main()