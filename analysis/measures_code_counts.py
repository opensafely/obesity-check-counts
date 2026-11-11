from ehrql import years, INTERVAL, Measures
from ehrql.tables.tpp import (
    practice_registrations,
    clinical_events
    )

measures = Measures()
measures.configure_disclosure_control(enabled=True)
measures.configure_dummy_data(population_size=5000)

measures.define_defaults(
    intervals=years(1).starting_on("2025-08-01"),
    denominator=practice_registrations.exists_for_patient_on(INTERVAL.start_date)
    )

codelists = {
    "obesity_med_referral": ["2386201000000107"],
    "obesity_med_unsuitable": ["2386221000000103"],
    "obesity_med_review": ["2386251000000108"],
    "obesity_med_started": ["2386231000000101"],
    "obesity_med_declined": ["2386241000000105"],
    "pancreas_cancer": ["2489011000000102"],
    "cataract_operation": ["434215004"],
    "ambulatory_bp": ["2314241000000104"],
    "serum_protein": ["1012151000000104"],
    "blood_glucose": ["774351000000102"]
}

code_count = {}

for name, codelist in codelists.items():
 
    code_count[name] = (
        clinical_events
        .where(clinical_events.date.is_during(INTERVAL))
        .where(clinical_events.snomedct_code.is_in(codelist))
        .count_for_patient()
    )

    measures.define_measure(
        name=f"{name}_count",
        numerator=code_count[name]
    )
