from repos.metric_repos import MetricRepos
#add metrics 
if __name__ == "__main__":
    metric_names = ["sgaRatio",
                     "randdRatio", 
                     "deprecationRatio",
                     "interestExpenseRatio",
                     "netEarningsRatio"]
    
    repos = MetricRepos()

    for metric_name in metric_names:
        repos.create_metric(metric_name=metric_name, metric_type="wb")


