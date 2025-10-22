# Publishing Memo

## Publishing Workflow

### TestPyPI (Testing Environment)

TestPyPI is a separate instance of PyPI for testing package uploads without affecting the production PyPI index.

#### Setup

1. **Register accounts**:

   - Production PyPI: [pypi.org/account/register/](https://pypi.org/account/register/)
   - Test PyPI: [test.pypi.org/account/register/](https://test.pypi.org/account/register/)

2. **Generate API tokens**:

   - Production: [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
   - TestPyPI: [test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)

3. **Configure authentication** in `~/.pypirc`:

   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR_PRODUCTION_API_TOKEN_HERE

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TEST_API_TOKEN_HERE
   ```

### Security Considerations

**Important**: PyPI packages are **immutable and access-controlled**. Understanding security is crucial:

#### Package Ownership and Access Control

1. **Package Names**: First-come, first-served basis

   - Once you register `uv-ps1-wrapper`, no one else can use this exact name
   - Package names are case-insensitive and treat hyphens/underscores as equivalent

2. **Access Permissions**:

   - **Owner**: Full control (you, as the package creator)
   - **Maintainer**: Can upload new versions (granted by Owner)
   - **No public write access**: Random users cannot modify your package

3. **Version Immutability**:
   - Once uploaded, a specific version (e.g., `0.1.0`) cannot be changed or deleted
   - Only new versions can be published
   - This ensures reproducible installations

#### Security Best Practices

1. **Account Security**:

   ```bash
   # Enable 2FA on your PyPI account (highly recommended)
   # Use strong, unique passwords
   # Regularly rotate API tokens
   ```

2. **API Token Management**:

   - Use scoped tokens (project-specific rather than global)
   - Store tokens securely (never in version control)
   - Rotate tokens periodically

3. **Package Verification**:

   ```bash
   # Always verify what you're uploading
   python -m twine check dist/*

   # Check package contents
   python -m zipfile -l dist/*.whl
   ```

4. **Code Signing** (Advanced):
   ```bash
   # Consider using sigstore for package signing (optional)
   pip install sigstore
   python -m sigstore sign dist/*
   ```

#### Common Security Threats

1. **Account Compromise**: Protect your PyPI credentials
2. **Typosquatting**: Be aware of similar package names
3. **Dependency Confusion**: Verify package sources
4. **Supply Chain Attacks**: Review dependencies regularly

#### Build and Upload Process

1. **Update version** in `pyproject.toml`:

   ```toml
   [project]
   name = "uv-ps1-wrapper"
   version = "0.1.2"  # Increment version
   ```

2. **Clean previous builds**:

   ```bash
   rm -rf dist/ build/ *.egg-info/
   # Or use uv to clean and build
   uv build --clean
   ```

3. **Build the package**:

   ```bash
   uv build
   ```

4. **Check the distribution**:

   ```bash
   uv run twine check dist/*
   ```

5. **Upload to TestPyPI**:

   ```bash
   uv run twine upload --repository testpypi dist/*
   ```

6. **Test installation from TestPyPI**:

   ```bash
   # Create a fresh virtual environment for testing
   uv venv test_env

   # Windows
   test_env\Scripts\activate
   # Unix/macOS
   # source test_env/bin/activate

   # Install from TestPyPI with uv
   uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ uv-ps1-wrapper

   # Test basic functionality
   python -c "
   import argparse
   from uv_ps1_wrapper import generate_ps1_wrapper
   parser = argparse.ArgumentParser()
   parser.add_argument('--test', help='Test argument')
   print('TestPyPI installation successful!')
   "

   # Clean up
   deactivate
   rm -rf test_env
   ```

### Automated Publishing with GitHub Actions

The repository includes automated publishing workflows that can deploy to TestPyPI and PyPI automatically.

#### Setup GitHub Secrets

1. **Generate API Tokens**:

   - TestPyPI: [test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)
   - PyPI: [pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)

2. **Add Secrets to GitHub Repository**:
   - Go to your repository on GitHub
   - Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token
     - `PYPI_API_TOKEN`: Your PyPI API token

#### Automated Deployment Triggers

1. **TestPyPI Deployment** (Automatic):

   ```yaml
   # Triggers on every push to main branch
   if: github.event_name == 'push' && github.ref == 'refs/heads/main'
   ```

   - Runs after successful tests and linting
   - Publishes to TestPyPI automatically
   - Uses `skip-existing: true` to avoid conflicts

2. **PyPI Deployment** (Tag-based):
   ```yaml
   # Triggers only on version tags (e.g., v0.1.0)
   if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
   ```
   - Requires creating a git tag: `git tag v0.1.0 && git push origin v0.1.0`
   - Only runs after successful TestPyPI deployment
   - Publishes to production PyPI

#### Manual Release Process

1. **Update version** in `pyproject.toml`:

   ```toml
   version = "0.1.2"  # Increment version
   ```

2. **Commit and push changes**:

   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.2"
   git push origin main
   ```

   ✅ **This automatically triggers TestPyPI deployment**

3. **Create and push tag for PyPI release**:
   ```bash
   git tag v0.1.2
   git push origin v0.1.2
   ```
   ✅ **This automatically triggers PyPI deployment**

#### Monitoring Deployments

- **GitHub Actions**: Check the "Actions" tab for deployment status
- **TestPyPI**: [test.pypi.org/project/uv-ps1-wrapper/](https://test.pypi.org/project/uv-ps1-wrapper/)
- **PyPI**: [pypi.org/project/uv-ps1-wrapper/](https://pypi.org/project/uv-ps1-wrapper/)

### Production PyPI

After successful testing on TestPyPI:

1. **Upload to production PyPI**:

   ```bash
   uv run twine upload dist/*
   ```

2. **Verify installation**:

   ```bash
   # Test in a fresh environment
   uv venv prod_test_env

   # Windows
   prod_test_env\Scripts\activate
   # Unix/macOS
   # source prod_test_env/bin/activate

   uv pip install uv-ps1-wrapper

   # Test functionality
   python -c "
   from uv_ps1_wrapper import generate_ps1_wrapper
   print('Production PyPI installation successful!')
   "

   # Clean up
   deactivate
   rm -rf prod_test_env
   ```

## Version Management

### Semantic Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): New functionality in a backwards compatible manner
- **PATCH** (0.0.1): Backwards compatible bug fixes

### Pre-release Versions

For testing purposes, you can use pre-release versions:

```toml
# Alpha release
version = "0.2.0a1"

# Beta release
version = "0.2.0b1"

# Release candidate
version = "0.2.0rc1"
```

## Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` or changelog section in `README.md`
- [ ] Run full test suite: `uv run pytest`
- [ ] Check code quality: `uv run ruff check src tests examples`
- [ ] Build package: `uv build`
- [ ] Check distribution: `uv run twine check dist/*`
- [ ] Upload to TestPyPI: `uv run twine upload --repository testpypi dist/*`
- [ ] Test TestPyPI installation
- [ ] Upload to production PyPI: `uv run twine upload dist/*`
- [ ] Test production PyPI installation
- [ ] Create GitHub release with tag
- [ ] Update documentation if needed

## Troubleshooting

### Common Issues

1. **"File already exists" error**:

   - You're trying to upload a version that already exists
   - Increment the version number in `pyproject.toml`

2. **Import errors after installation**:

   - Check that package structure matches imports
   - Verify `__init__.py` exports are correct

3. **Authentication failures**:

   - Verify API token is correct
   - Check `~/.pypirc` configuration
   - Ensure you're using `__token__` as username

4. **Build failures**:

   - Check `pyproject.toml` syntax
   - Verify all required files are present
   - Clean build artifacts and retry

5. **Security-related issues**:
   - **"Package name taken"**: Choose a different name, someone else registered it first
   - **"Insufficient permissions"**: You don't have maintainer access to this package
   - **"Invalid credentials"**: Check your API token or enable 2FA if required
   - **"Package appears suspicious"**: PyPI may flag packages for manual review

### Security Verification Commands

```bash
# Verify package ownership before uploading
python -c "
import requests
resp = requests.get('https://pypi.org/pypi/uv-ps1-wrapper/json')
if resp.status_code == 200:
    owner = resp.json()['info']['maintainer'] or resp.json()['info']['author']
    print(f'Package owner: {owner}')
else:
    print('Package not found (available for registration)')
"

# Check for similar package names (typosquatting prevention)
pip search argparse  # Note: pip search is deprecated, use PyPI web interface

# Verify package integrity after installation
pip show uv-ps1-wrapper
pip check  # Check for dependency conflicts
```

### Useful Commands

```bash
# Check package structure
python -c "import uv_ps1_wrapper; print(uv_ps1_wrapper.__file__)"

# List package contents
uv run python -m zipfile -l dist/*.whl

# Examine package metadata
uv run twine check dist/* --strict

# Clean build artifacts
rm -rf build/ dist/ *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Alternative: use uv for cleaning and building
uv build --clean
```
