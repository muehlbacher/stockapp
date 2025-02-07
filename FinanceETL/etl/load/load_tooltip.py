from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from FinanceETL.db.models import Metric, MetricTooltip


class TooltipLoader:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def load_tooltip(self, metric_name: str, tooltip: str):
        try:
            # Find the metric by name
            metric = (
                self.db_session.query(Metric).filter_by(MetricName=metric_name).one()
            )

            # Check if a tooltip already exists for this metric
            existing_tooltip = (
                self.db_session.query(MetricTooltip)
                .filter_by(MetricID=metric.MetricID)
                .first()
            )

            if existing_tooltip:
                # Update existing tooltip
                existing_tooltip.Tooltip = tooltip
            else:
                # Insert new tooltip
                new_tooltip = MetricTooltip(MetricID=metric.MetricID, Tooltip=tooltip)
                self.db_session.add(new_tooltip)

            # Commit changes
            self.db_session.commit()

        except NoResultFound:
            print(f"Metric '{metric_name}' not found in the database.")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error while loading tooltip: {e}")

    def remove_tooltip(self, metric_name: str):
        try:
            # Find the metric by name
            metric = (
                self.db_session.query(Metric).filter_by(MetricName=metric_name).one()
            )

            # Check if a tooltip exists for this metric
            tooltip = (
                self.db_session.query(MetricTooltip)
                .filter_by(MetricID=metric.MetricID)
                .first()
            )

            if tooltip:
                self.db_session.delete(tooltip)
                self.db_session.commit()
                print(f"Tooltip for '{metric_name}' removed successfully.")
            else:
                print(f"No tooltip found for metric '{metric_name}'.")

        except NoResultFound:
            print(f"Metric '{metric_name}' not found in the database.")
        except Exception as e:
            self.db_session.rollback()
            print(f"Error while removing tooltip: {e}")
