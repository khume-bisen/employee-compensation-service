from typing import List, Dict, Any, Optional

from repositories.report_repository import ReportRepository


class ReportService:

    def __init__(self):
        self.repository = ReportRepository()

    def get_total_bonus(self) -> float:
        return self.repository.get_total_bonus()

    def get_employees_with_no_bonus(self) -> List[Dict[str, Any]]:
        return self.repository.get_employees_with_no_bonus()

    def get_bonus_percentage(self) -> List[Dict[str, Any]]:
        return self.repository.get_bonus_percentage()

    def get_department_bonus(self) -> List[Dict[str, Any]]:
        return self.repository.get_department_bonus()

    def get_bonus_ranking(self) -> List[Dict[str, Any]]:
        return self.repository.get_bonus_ranking()

    def get_highest_salary(self) -> Optional[Dict[str, Any]]:
        return self.repository.get_highest_salary()

    def get_highest_total_compensation(self) -> Optional[Dict[str, Any]]:
        return self.repository.get_highest_total_compensation()