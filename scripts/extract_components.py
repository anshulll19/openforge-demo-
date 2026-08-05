import csv
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass
class Component:
    reference: str
    library: str
    deviceset: str
    device: str
    value: str


def parse_schematic(sch_path: Path) -> list[Component]:
    tree = ET.parse(sch_path)
    root = tree.getroot()
    parts_elem = root.find(".//parts")
    
    components = []
    if parts_elem is not None:
        for part in parts_elem.findall("part"):
            ref = part.get("name", "")
            library = part.get("library", "")
            deviceset = part.get("deviceset", "")
            device = part.get("device", "")
            value = part.get("value", "")
            
            components.append(
                Component(
                    reference=ref,
                    library=library,
                    deviceset=deviceset,
                    device=device,
                    value=value,
                )
            )
            
    return components


def write_csv(parts: list[Component], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reference", "Library", "DeviceSet", "Device", "Value"])
        for part in parts:
            writer.writerow(
                [part.reference, part.library, part.deviceset, part.device, part.value]
            )


def write_json(parts: list[Component], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    data = [asdict(part) for part in parts]
    with output.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    sch_path = (
        base_dir
        / "projects"
        / "Arduino_Uno_R3"
        / "docs"
        / "Arduino_Uno_R3_CAD"
        / "UNO-TH_Rev3e.sch"
    )
    bom_dir = base_dir / "projects" / "Arduino_Uno_R3" / "bom"

    components = parse_schematic(sch_path)
    write_csv(components, bom_dir / "component_inventory.csv")
    write_json(components, bom_dir / "component_inventory.json")


if __name__ == "__main__":
    main()