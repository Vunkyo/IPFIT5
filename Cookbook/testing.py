import evidence_metadata
import open_evidence
import RecursingToCsv
import extract_file_type

evidence_metadata.main("../RawTestImage.dd", "raw", None)
RecursingToCsv.main("../RawTestImage.dd", "raw", "recursing.csv", None)
extract_file_type.main("../RawTestImage.dd", "raw", "jpg", "/extracted/jpg/", "DOS")
open_evidence.main("../RawTestImage.dd", "raw", 32256)

