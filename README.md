# DaScient Energy, Weather, and Interoperability Suite

A notebook-first toolkit for:

- Deep and Generative AI analytics and open-source metrics design
- Data center interoperability performance metrics and mitigation protocols under energy and grid stress
- Open-source RSS and weather driven energy intelligence for data center planning

## Included notebooks

- `notebooks/DaScient_DeepGenAI_Analytics_OpenSource_Metrics_Package.ipynb`
- `notebooks/DaScient_DataCenter_Interop_EnergyCrisis_Notebook.ipynb`
- `notebooks/DaScient_Weather_News_Energy_DataCenter_Planning.ipynb`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
jupyter lab
```

## Repo layout

- `notebooks/` - the main packages
- `src/dascient_suite/` - reusable modules (RSS, weather, energy proxies, reporting I/O)
- `docs/` - playbooks and glossary
- `reports/` - generated exports (optional)
- `data/sample/` - sample schemas

## License

MIT - see `LICENSE`.

## Disclaimer

Planning-grade analytics and operational scaffolding. Not a substitute for facility engineering, safety review, or regulatory compliance.
