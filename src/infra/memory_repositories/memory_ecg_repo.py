from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.errors.ecg_not_found_error import ECGNotFoundError
from src.domain.ecg.lead import Lead
from src.infra.storage import ECGModel, LeadModel, Storage
from utils.date_converter import date_to_str, str_to_date


@dataclass
class MemoryECGRepository:
    connection: Storage

    def save(self, ecg: Electrocardiogram) -> None:
        self.connection.ecgs.append(self.__to_storage(ecg))

    def get(self, id: str) -> Electrocardiogram:
        try:
            result = next((ecg for ecg in self.connection.ecgs if ecg["id"] == id))
        except StopIteration:
            raise ECGNotFoundError

        return self.__to_ecg(result)

    def __to_storage(self, ecg: Electrocardiogram) -> ECGModel:
        def lead_to_storage(lead: Lead) -> LeadModel:
            return {
                "name": lead.name,
                "n_samples": lead.n_samples,
                "signal": ",".join([str(signal) for signal in lead.signal]),
            }

        return {
            "id": ecg.id,
            "date": date_to_str(ecg.date),
            "leads": [lead_to_storage(lead) for lead in ecg.leads],
            "zero_crossings": ecg.zero_crossings,
            "uploader_id": ecg.uploader_id,
        }

    def __to_ecg(self, storage_ecg: ECGModel) -> Electrocardiogram:
        def storage_to_lead(storage_lead: LeadModel) -> Lead:
            return Lead(
                name=storage_lead["name"],
                n_samples=storage_lead["n_samples"],
                signal=[int(value) for value in storage_lead["signal"].split(",")],
            )

        return Electrocardiogram(
            id=storage_ecg["id"],
            date=str_to_date(storage_ecg["date"]),
            leads=[storage_to_lead(lead) for lead in storage_ecg["leads"]],
            zero_crossings=storage_ecg["zero_crossings"],
            uploader_id=storage_ecg["uploader_id"],
        )
