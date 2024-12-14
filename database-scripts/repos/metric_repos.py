from models.models import Metric
from repos.base_repos import BaseRepos


class MetricRepos(BaseRepos):
    def create_metric(self, metric_name: str, metric_type: str = None):
        metric = Metric(MetricName=metric_name, MetricType=metric_type)
        self.session.add(metric)
        return self.session.commit()
    
    def retrieve_metric(self, metric_name: str):
        metric = self.session.query(Metric).filter_by(MetricName=metric_name).limit(1).all()
        return metric[0]
