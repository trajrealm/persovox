import json
from pathlib import Path

def merge_resume_jsons(json_folder: str) -> dict:
    merged = {
        "personal_info": {
        "name": None,
        "email": None,
        "phone": None,
        "address": None,
        "linkedin": None
        },
        "summary": "",
        "highlights": [],
        "experiences": [],
        "education": [],
        "skills": set(),
        "certifications": []
    }

    seen_exp = set()
    seen_edu = set()
    seen_cert = set()

    json_files = list(Path(json_folder).glob("*.json"))

    for jf in json_files:
        with open(jf, "r") as f:
            j = json.load(f)

        merged["personal_info"]["name"] = merged["personal_info"]["name"] or j.get("name")
        merged["personal_info"]["email"] = merged["personal_info"]["email"] or j.get("email")
        merged["personal_info"]["phone"] = merged["personal_info"]["phone"] or j.get("phone")
        merged["personal_info"]["address"] = merged["personal_info"]["address"] or j.get("address")
        merged["personal_info"]["linkedin"] = merged["personal_info"]["linkedin"] or j.get("linkedin")

        if j.get("summary"):
            merged["summary"] += "\n" + j["summary"]
        
        for high in j.get("highlights", []):
            merged["highlights"].append(high)

        for exp in j.get("experiences", []):
            key = (exp.get("job_title"), exp.get("company"), exp.get("start_date"))
            if key not in seen_exp:
                merged["experiences"].append(exp)
                seen_exp.add(key)

        for edu in j.get("education", []):
            key = (edu.get("degree"), edu.get("university"))
            if key not in seen_edu:
                merged["education"].append(edu)
                seen_edu.add(key)

        for cert in j.get("certifications", []):
            key = (cert.get("name"), cert.get("issuer", ""))
            if key not in seen_cert:
                merged["certifications"].append(cert)
                seen_cert.add(key)

        merged["skills"].update(j.get("skills", []))

    merged["skills"] = sorted(list(merged["skills"]))

    return merged


if __name__ == "__main__":
    for user in ["triloke", "qureena"]:
        merged_data = merge_resume_jsons(f"data/{user}/resumes/parsed")
        with open(f"data/{user}/resumes/parsed/merged.json", "w") as f:
            json.dump(merged_data, f, indent=2)
