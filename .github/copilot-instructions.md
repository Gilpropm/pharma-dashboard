# AI Coding Agent Instructions for Pharma Dashboard

## Project Overview
This is a **Streamlit web application** serving as a pharma (pharmaceutical) dashboard. Currently a template, it's designed for rapid interactive data visualization and real-time updates.

**Key Architecture**: Single-file application ([streamlit_app.py](../streamlit_app.py)) pattern. All UI and logic flows through Streamlit's reactive framework.

## Essential Developer Workflows

### Running the Application
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
**Dev Container Note**: The Codespaces setup auto-starts Streamlit on port 8501 with CORS/CSRF disabled. See [.devcontainer/devcontainer.json](..) for details.

### Adding Dependencies
1. Add package to [requirements.txt](../requirements.txt)
2. Reinstall: `pip install -r requirements.txt`
3. The dev container's `updateContentCommand` handles automatic installation

## Streamlit-Specific Patterns

### State Management
- Use `@st.cache_data` for expensive computations that don't depend on user input
- Use `@st.cache_resource` for database connections, ML models
- Avoid storing mutable state outside of `st.session_state` (only works within a user session)

### UI Layout Structure
```python
st.title("Title")  # Main header
st.write("Description")  # Content
col1, col2 = st.columns(2)  # Side-by-side layout
with col1: st.metric("Label", value)  # Dashboard metrics
```

### Pharma Dashboard Considerations
- Performance: Streamlit reruns entire script on interaction—optimize with caching
- Data updates: Use `st.session_state` for interactive filters, `@st.cache_data` for drug/patient data queries
- Real-time metrics: Consider polling patterns or external data sources (databases, APIs)

## Project-Specific Conventions

- **Single entry point**: All features go in [streamlit_app.py](../streamlit_app.py) until complexity warrants modularization
- **Python environment**: Python 3.11 (locked in dev container)
- **Extensions**: Uses ms-python.python and ms-python.vscode-pylance for IDE support
- **Port**: Streamlit app runs on port 8501 locally

## Cross-Component Communication

Since this is a single-file template, all communication is through:
- Streamlit's widget callbacks and `st.session_state`
- External APIs (when pharma data sources are added)
- Files in the project directory

## Testing & Quality

No CI/CD or testing framework configured yet. Consider adding:
- `pytest` for unit tests
- `pylint` or `flake8` for linting (add to dev container extensions)

---

**As the pharma dashboard evolves**, split [streamlit_app.py](../streamlit_app.py) into modules:
- `pages/` (multi-page app structure)
- `utils/data.py` (data fetching/transformation)
- `utils/metrics.py` (pharma-specific calculations)
