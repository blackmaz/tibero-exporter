import logging


# 로깅 설정
logger = logging.getLogger(__name__)


class TiberoCollector:

    def __init__(self, db_manager, metric_definitions):
        self.db = db_manager
        self.metric_definitions = metric_definitions

    def fetch_raw_metrics(self):
        results = {}
        if not self.db.is_connected():
            self.db.connect()
        conn = self.db.get_connection()
        cursor = conn.cursor()

        for key, meta in self.metric_definitions.items():
            query = meta.get("query")
            if not query:
                continue
            try:
                cursor.execute(query)
                result = cursor.fetchone()
                logger.debug(f"{key} 수집 완료: {result}")
                if result and result[0] is not None:
                    results[key] = result[0]
            except Exception as e:
                logger.warning(f"{key} 수집 실패: {e}")
        cursor.close()
        return results
