from dataclasses import dataclass
from src.domain.ecg.ecg import Electrocardiogram
from src.domain.ecg.lead import Lead
from src.infra.storage import ECGModel, LeadModel, Storage


@dataclass
class MemoryECGRepository:
    connection: Storage

    def save(self, ecg: Electrocardiogram) -> None:
        self.connection.ecgs.append(self.__to_storage(ecg))

    def get(self, id: str) -> Electrocardiogram:
        pass

    def __to_storage(self, ecg: Electrocardiogram) -> ECGModel:
        def lead_to_storage(lead: Lead) -> LeadModel:
            return {
                "name": lead.name,
                "n_samples": lead.n_samples,
                "signal": ",".join([str(signal) for signal in lead.signal]),
            }

        return {
            "id": ecg.id,
            "date": str(ecg.date),
            "leads": [lead_to_storage(lead) for lead in ecg.leads],
        }
