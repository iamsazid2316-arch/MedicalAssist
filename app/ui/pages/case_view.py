from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
)


class CaseView(QWidget):
    def __init__(self):
        super().__init__()

        self.current_case_id = ""

        self.saved_diagnoses = {}
        self.saved_treatments = {}
        self.saved_notes = {}

        # =====================================================
        # SCROLL AREA
        # =====================================================

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()

        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(
            40, 30, 40, 30
        )
        main_layout.setSpacing(12)

        # =====================================================
        # PAGE TITLE
        # =====================================================

        title = QLabel("Medical Case")
        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        # =====================================================
        # PATIENT INFORMATION
        # =====================================================

        patient_title = QLabel("Patient Information")
        patient_title.setAlignment(Qt.AlignCenter)

        self.patient_info = QLabel(
            "No case selected."
        )
        self.patient_info.setAlignment(Qt.AlignCenter)
        self.patient_info.setWordWrap(True)

        main_layout.addWidget(patient_title)
        main_layout.addWidget(self.patient_info)

        main_layout.addSpacing(15)

        # =====================================================
        # CASE STATUS
        # =====================================================

        self.status = QLabel(
            "Case Status: Pending"
        )
        self.status.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(self.status)

        main_layout.addSpacing(15)

        # =====================================================
        # SYMPTOMS
        # =====================================================

        symptoms_title = QLabel("Symptoms")
        symptoms_title.setAlignment(Qt.AlignCenter)

        self.symptoms = QLabel(
            "No symptoms available."
        )
        self.symptoms.setAlignment(Qt.AlignCenter)
        self.symptoms.setWordWrap(True)

        main_layout.addWidget(symptoms_title)
        main_layout.addWidget(self.symptoms)

        main_layout.addSpacing(15)

        # =====================================================
        # DIAGNOSIS
        # =====================================================

        diagnosis_title = QLabel("Diagnosis")
        diagnosis_title.setAlignment(Qt.AlignCenter)

        self.diagnosis_input = QTextEdit()
        self.diagnosis_input.setPlaceholderText(
            "Enter diagnosis for this case..."
        )
        self.diagnosis_input.setMinimumHeight(90)
        self.diagnosis_input.setMaximumHeight(130)

        self.save_diagnosis_button = QPushButton(
            "Save Diagnosis"
        )
        self.save_diagnosis_button.setMinimumHeight(40)

        self.diagnosis_status = QLabel("")
        self.diagnosis_status.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(diagnosis_title)
        main_layout.addWidget(self.diagnosis_input)
        main_layout.addWidget(
            self.save_diagnosis_button
        )
        main_layout.addWidget(
            self.diagnosis_status
        )

        main_layout.addSpacing(15)

        # =====================================================
        # TREATMENT
        # =====================================================

        treatment_title = QLabel(
            "Treatment / Recommendation"
        )
        treatment_title.setAlignment(Qt.AlignCenter)

        self.treatment_input = QTextEdit()
        self.treatment_input.setPlaceholderText(
            "Enter treatment or recommendation..."
        )
        self.treatment_input.setMinimumHeight(90)
        self.treatment_input.setMaximumHeight(130)

        self.save_treatment_button = QPushButton(
            "Save Treatment / Recommendation"
        )
        self.save_treatment_button.setMinimumHeight(40)

        self.treatment_status = QLabel("")
        self.treatment_status.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(treatment_title)
        main_layout.addWidget(self.treatment_input)
        main_layout.addWidget(
            self.save_treatment_button
        )
        main_layout.addWidget(
            self.treatment_status
        )

        main_layout.addSpacing(15)

        # =====================================================
        # CONSULTATION HISTORY
        # =====================================================

        consultation_title = QLabel(
            "Consultation History"
        )
        consultation_title.setAlignment(
            Qt.AlignCenter
        )

        self.consultation_history = QLabel(
            "No previous consultation recorded."
        )
        self.consultation_history.setAlignment(
            Qt.AlignCenter
        )
        self.consultation_history.setWordWrap(True)

        main_layout.addWidget(
            consultation_title
        )
        main_layout.addWidget(
            self.consultation_history
        )

        main_layout.addSpacing(15)

        # =====================================================
        # CASE NOTES
        # =====================================================

        notes_title = QLabel("Case Notes")
        notes_title.setAlignment(Qt.AlignCenter)

        self.case_notes = QTextEdit()
        self.case_notes.setPlaceholderText(
            "Enter notes about this medical case..."
        )
        self.case_notes.setMinimumHeight(90)
        self.case_notes.setMaximumHeight(130)

        self.save_notes_button = QPushButton(
            "Save Notes"
        )
        self.save_notes_button.setMinimumHeight(40)

        self.notes_status = QLabel("")
        self.notes_status.setAlignment(
            Qt.AlignCenter
        )

        main_layout.addWidget(notes_title)
        main_layout.addWidget(self.case_notes)
        main_layout.addWidget(
            self.save_notes_button
        )
        main_layout.addWidget(
            self.notes_status
        )

        main_layout.addSpacing(15)

        # =====================================================
        # DOCTOR ACTIONS
        # =====================================================

        actions_title = QLabel("Doctor Actions")
        actions_title.setAlignment(
            Qt.AlignCenter
        )

        self.approve_button = QPushButton(
            "Approve Case"
        )
        self.approve_button.setMinimumHeight(40)

        self.reject_button = QPushButton(
            "Reject Case"
        )
        self.reject_button.setMinimumHeight(40)

        main_layout.addWidget(actions_title)

        main_layout.addWidget(
            self.approve_button
        )

        main_layout.addWidget(
            self.reject_button
        )

        main_layout.addSpacing(10)

        # =====================================================
        # BACK BUTTON
        # =====================================================

        self.back_button = QPushButton(
            "Back to Doctor Dashboard"
        )
        self.back_button.setMinimumHeight(40)

        main_layout.addWidget(
            self.back_button
        )

        main_layout.addSpacing(20)

        # =====================================================
        # CONTENT SIZE
        # =====================================================

        content.setMaximumWidth(950)

        wrapper = QWidget()

        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(
            0, 0, 0, 0
        )

        wrapper_layout.addStretch()
        wrapper_layout.addWidget(content)
        wrapper_layout.addStretch()

        scroll.setWidget(wrapper)

        # =====================================================
        # MAIN PAGE LAYOUT
        # =====================================================

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(
            0, 0, 0, 0
        )

        page_layout.addWidget(scroll)

        # =====================================================
        # SIGNALS
        # =====================================================

        self.save_diagnosis_button.clicked.connect(
            self.save_diagnosis
        )

        self.save_treatment_button.clicked.connect(
            self.save_treatment
        )

        self.save_notes_button.clicked.connect(
            self.save_notes
        )

        self.approve_button.clicked.connect(
            self.approve_case
        )

        self.reject_button.clicked.connect(
            self.reject_case
        )

    # =====================================================
    # LOAD CASE
    # =====================================================

    def load_case(self, case_id, case_data):

        self.current_case_id = case_id

        details = case_data.get(
            "details",
            ""
        )

        summary = case_data.get(
            "summary",
            ""
        )

        self.patient_info.setText(
            "Case ID: "
            + case_id
            + "\n"
            + self.extract_detail(
                details,
                "Patient"
            )
            + "\n"
            + self.extract_detail(
                details,
                "Age"
            )
            + "\n"
            + self.extract_detail(
                details,
                "Gender"
            )
            + "\n"
            + self.extract_detail(
                details,
                "Priority"
            )
        )

        self.symptoms.setText(
            summary
        )

        self.consultation_history.setText(
            case_data.get(
                "consultation_history",
                "No previous consultation recorded."
            )
        )

        self.diagnosis_input.setPlainText(
            self.saved_diagnoses.get(
                case_id,
                ""
            )
        )

        self.treatment_input.setPlainText(
            self.saved_treatments.get(
                case_id,
                ""
            )
        )

        self.case_notes.setPlainText(
            self.saved_notes.get(
                case_id,
                ""
            )
        )

        self.status.setText(
            "Case Status: Pending"
        )

        self.diagnosis_status.clear()
        self.treatment_status.clear()
        self.notes_status.clear()

    # =====================================================
    # EXTRACT DETAIL
    # =====================================================

    def extract_detail(self, details, field):

        for line in details.splitlines():

            if line.startswith(
                field + ":"
            ):
                return line

        return f"{field}: Not available"

    # =====================================================
    # SAVE DIAGNOSIS
    # =====================================================

    def save_diagnosis(self):

        if not self.current_case_id:

            self.diagnosis_status.setText(
                "No case selected."
            )

            return

        diagnosis = (
            self.diagnosis_input
            .toPlainText()
            .strip()
        )

        if not diagnosis:

            self.diagnosis_status.setText(
                "Please enter a diagnosis."
            )

            return

        self.saved_diagnoses[
            self.current_case_id
        ] = diagnosis

        self.diagnosis_status.setText(
            "Diagnosis saved successfully."
        )

    # =====================================================
    # SAVE TREATMENT
    # =====================================================

    def save_treatment(self):

        if not self.current_case_id:

            self.treatment_status.setText(
                "No case selected."
            )

            return

        treatment = (
            self.treatment_input
            .toPlainText()
            .strip()
        )

        if not treatment:

            self.treatment_status.setText(
                "Please enter a treatment or recommendation."
            )

            return

        self.saved_treatments[
            self.current_case_id
        ] = treatment

        self.treatment_status.setText(
            "Treatment saved successfully."
        )

    # =====================================================
    # SAVE NOTES
    # =====================================================

    def save_notes(self):

        if not self.current_case_id:

            self.notes_status.setText(
                "No case selected."
            )

            return

        notes = (
            self.case_notes
            .toPlainText()
            .strip()
        )

        self.saved_notes[
            self.current_case_id
        ] = notes

        self.notes_status.setText(
            "Notes saved successfully."
        )

    # =====================================================
    # APPROVE CASE
    # =====================================================

    def approve_case(self):

        if not self.current_case_id:
            return

        self.status.setText(
            "Case Status: Approved"
        )

    # =====================================================
    # REJECT CASE
    # =====================================================

    def reject_case(self):

        if not self.current_case_id:
            return

        self.status.setText(
            "Case Status: Rejected"
        )