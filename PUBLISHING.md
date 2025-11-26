# Publishing nasdaqapi to PyPI - Setup Guide

## Using Trusted Publishing (No API Tokens Required!)

PyPI now supports **Trusted Publishing** which uses OpenID Connect (OIDC) to verify GitHub Actions workflows. This is more secure than API tokens and is the recommended approach.

## Setup Steps

### 1. Create PyPI Account (If You Don't Have One)

1. Go to https://pypi.org/account/register/
2. Create your account
3. Verify your email address

### 2. Configure Trusted Publishing on PyPI

#### For TestPyPI (Recommended First Test):

1. Go to https://test.pypi.org/manage/account/publishing/
2. Click **"Add a new pending publisher"**
3. Fill in the form:
   - **PyPI Project Name**: `nasdaqapi`
   - **Owner**: `deepentropy` (your GitHub username/org)
   - **Repository name**: `nasdaqapi`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `testpypi`
4. Click **"Add"**

#### For PyPI (Production):

1. Go to https://pypi.org/manage/account/publishing/
2. Click **"Add a new pending publisher"**
3. Fill in the form:
   - **PyPI Project Name**: `nasdaqapi`
   - **Owner**: `deepentropy`
   - **Repository name**: `nasdaqapi`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click **"Add"**

### 3. Test with TestPyPI (Optional but Recommended)

1. Go to https://github.com/deepentropy/nasdaqapi/actions/workflows/publish.yml
2. Click **"Run workflow"**
3. Select branch: `main`
4. Click **"Run workflow"**
5. Wait for the workflow to complete
6. Check https://test.pypi.org/project/nasdaqapi/

If successful, you'll see:
```bash
# You can test install from TestPyPI
pip install -i https://test.pypi.org/simple/ nasdaqapi
```

### 4. Publish to PyPI (Production)

#### Option A: Create Release via GitHub UI

1. Go to https://github.com/deepentropy/nasdaqapi/releases
2. Click **"Create a new release"**
3. Click **"Choose a tag"** → Type `v0.1.0` → **"Create new tag: v0.1.0 on publish"**
4. Release title: `v0.1.0`
5. Description:
   ```markdown
   ## Initial Release
   
   - Complete NASDAQ API wrapper
   - Fetch quotes, financials, dividends, ownership data
   - Normalized data structure
   - 14 data categories from NASDAQ API
   ```
6. Click **"Publish release"**
7. The workflow will automatically run and publish to PyPI!

#### Option B: Create Release via Command Line

```bash
cd C:\Users\otrem\PycharmProjects\nasdaqapi

# Create and push tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Then create the release on GitHub UI
```

### 5. Verify Publication

After the workflow completes:

1. Check https://pypi.org/project/nasdaqapi/
2. Your package should be live!

Install it anywhere:
```bash
pip install nasdaqapi
```

## Troubleshooting

### "Publisher Already Exists"

If you get this error when setting up trusted publishing:
- The package name might already be taken
- Try a different name like `nasdaq-api-python` or `nasdaq-data-api`
- Update `pyproject.toml` with the new name

### "Environment not found"

Make sure you created the GitHub environments:
1. Go to https://github.com/deepentropy/nasdaqapi/settings/environments
2. Create environment: `testpypi`
3. Create environment: `pypi`

### Workflow Fails

Check the logs at:
https://github.com/deepentropy/nasdaqapi/actions

Common issues:
- Trusted publishing not set up on PyPI
- Environment names don't match (`pypi` vs `testpypi`)
- Package name already exists on PyPI

## After Publishing

### Update stockfundamentals

Once published to PyPI, the stockfundamentals workflow will automatically install it:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt  # Will install nasdaqapi from PyPI
```

No changes needed! It will just work.

### Version Updates

For future updates:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Commit changes:
   ```bash
   git commit -am "Bump version to 0.2.0"
   git push
   ```

3. Create new release:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   # Then create release on GitHub
   ```

4. Workflow auto-publishes!

## Summary

✅ No API tokens needed  
✅ More secure than tokens  
✅ Automatic publishing on release  
✅ Can test with TestPyPI first  
✅ Simple version management  

**Just set up trusted publishing on PyPI once, then create releases on GitHub!** 🚀
