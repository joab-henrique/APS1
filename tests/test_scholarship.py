import dataclasses

import pytest

from codigo_original import EvaluationResult, Status, evaluate_scholarship


class TestApproved:
    def test_all_requirements_met(self):
        result = evaluate_scholarship(
            age=20,
            gpa=8.5,
            attendance_rate=92.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.APPROVED
        assert result.status.value == "APPROVED"
        assert result.reasons == ["Applicant meets all scholarship requirements."]

    def test_age_18_is_approved(self):
        result = evaluate_scholarship(
            age=18,
            gpa=8.0,
            attendance_rate=90.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.APPROVED
        assert result.reasons == ["Applicant meets all scholarship requirements."]


class TestManualReview:
    def test_review_with_all_three_review_reasons(self):
        # idade, gpa e frequência todos na faixa de revisão ao mesmo tempo
        result = evaluate_scholarship(
            age=17,
            gpa=6.5,
            attendance_rate=77.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.MANUAL_REVIEW
        assert result.status.value == "MANUAL_REVIEW"
        assert result.reasons == [
            "Applicant is under 18 and requires manual review.",
            "GPA is in the manual review range.",
            "Attendance rate is in the manual review range.",
        ]

    def test_review_due_to_age_only(self):
        result = evaluate_scholarship(
            age=17,
            gpa=8.0,
            attendance_rate=90.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.MANUAL_REVIEW
        assert result.reasons == [
            "Applicant is under 18 and requires manual review."
        ]


class TestRejected:
    def test_rejected_due_to_age(self):
        result = evaluate_scholarship(
            age=15,
            gpa=8.0,
            attendance_rate=90.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.REJECTED
        assert result.status.value == "REJECTED"
        assert result.reasons == ["Applicant is younger than the minimum age."]

    def test_rejected_due_to_missing_required_courses(self):
        result = evaluate_scholarship(
            age=20,
            gpa=8.0,
            attendance_rate=90.0,
            has_required_courses=False,
            disciplinary_record=False,
        )
        assert result.status == Status.REJECTED
        assert result.reasons == ["Required courses have not been completed."]

    def test_rejected_due_to_disciplinary_record(self):
        result = evaluate_scholarship(
            age=20,
            gpa=8.0,
            attendance_rate=90.0,
            has_required_courses=True,
            disciplinary_record=True,
        )
        assert result.status == Status.REJECTED
        assert result.reasons == ["Applicant has a disciplinary record."]

    def test_rejected_due_to_low_attendance(self):
        result = evaluate_scholarship(
            age=20,
            gpa=8.0,
            attendance_rate=0.0,
            has_required_courses=True,
            disciplinary_record=False,
        )
        assert result.status == Status.REJECTED
        assert result.reasons == [
            "Attendance rate is below the minimum required."
        ]


class TestInvalidInputs:
    def test_gpa_below_zero_raises(self):
        with pytest.raises(ValueError) as exc_info:
            evaluate_scholarship(
                age=20,
                gpa=-0.1,
                attendance_rate=90.0,
                has_required_courses=True,
                disciplinary_record=False,
            )
        assert str(exc_info.value) == "GPA must be between 0 and 10."

    def test_attendance_above_hundred_raises(self):
        with pytest.raises(ValueError) as exc_info:
            evaluate_scholarship(
                age=20,
                gpa=8.0,
                attendance_rate=150.0,
                has_required_courses=True,
                disciplinary_record=False,
            )
        assert str(exc_info.value) == "Attendance rate must be between 0 and 100."

    def test_gpa_above_ten_raises(self):
        with pytest.raises(ValueError) as exc_info:
            evaluate_scholarship(
                age=20,
                gpa=10.1,
                attendance_rate=90.0,
                has_required_courses=True,
                disciplinary_record=False,
            )
        assert str(exc_info.value) == "GPA must be between 0 and 10."


class TestBoundaryValues:
    # fronteira 6.0/7.0 do gpa: reject e ok
    def test_gpa_5_9_is_rejected(self):
        result = evaluate_scholarship(20, 5.9, 90.0, True, False)
        assert result.status == Status.REJECTED
        assert result.reasons == ["GPA is below the minimum required."]

    def test_gpa_6_0_is_review(self):
        result = evaluate_scholarship(20, 6.0, 90.0, True, False)
        assert result.status == Status.MANUAL_REVIEW
        assert result.reasons == ["GPA is in the manual review range."]

    def test_gpa_0_0_does_not_raise(self):
        # 0.0 é o piso do domínio válido, não pode estourar ValueError
        result = evaluate_scholarship(20, 0.0, 90.0, True, False)
        assert result.status == Status.REJECTED
        assert result.reasons == ["GPA is below the minimum required."]

    def test_gpa_7_0_is_approved(self):
        result = evaluate_scholarship(20, 7.0, 90.0, True, False)
        assert result.status == Status.APPROVED
        assert result.reasons == ["Applicant meets all scholarship requirements."]

    def test_gpa_10_0_is_approved(self):
        result = evaluate_scholarship(20, 10.0, 90.0, True, False)
        assert result.status == Status.APPROVED
        assert result.reasons == ["Applicant meets all scholarship requirements."]

    # fronteira 75.0/80.0 da frequência: reject e ok
    def test_attendance_74_9_is_rejected(self):
        result = evaluate_scholarship(20, 8.0, 74.9, True, False)
        assert result.status == Status.REJECTED
        assert result.reasons == ["Attendance rate is below the minimum required."]

    def test_attendance_80_0_is_approved(self):
        result = evaluate_scholarship(20, 8.0, 80.0, True, False)
        assert result.status == Status.APPROVED
        assert result.reasons == ["Applicant meets all scholarship requirements."]

    def test_attendance_75_0_is_review(self):
        result = evaluate_scholarship(20, 8.0, 75.0, True, False)
        assert result.status == Status.MANUAL_REVIEW
        assert result.reasons == [
            "Attendance rate is in the manual review range."
        ]

    def test_attendance_100_0_is_approved(self):
        result = evaluate_scholarship(20, 8.0, 100.0, True, False)
        assert result.status == Status.APPROVED
        assert result.reasons == ["Applicant meets all scholarship requirements."]

    def test_age_16_is_review(self):
        result = evaluate_scholarship(16, 8.0, 90.0, True, False)
        assert result.status == Status.MANUAL_REVIEW
        assert result.reasons == [
            "Applicant is under 18 and requires manual review."
        ]


class TestResultContract:
    def test_evaluation_result_is_immutable(self):
        # frozen=True: reatribuir campo depois de criado tem que dar erro
        result = evaluate_scholarship(20, 8.0, 90.0, True, False)
        with pytest.raises(dataclasses.FrozenInstanceError):
            result.status = Status.REJECTED
