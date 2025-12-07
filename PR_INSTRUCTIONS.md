# Pull Request Anleitung

## Schnell-Anleitung: PR erstellen

1. **Öffne diesen Link in deinem Browser:**
   ```
   https://github.com/7d3c/ai-counsel/compare/master...claude/ai-counsel-private-setup-01VK42FyrQcfttEDqr9tEqhL
   ```

2. **Klicke auf "Create pull request"**

3. **Titel:** `Add Docker deployment and direct API integrations`

4. **Beschreibung:**
   ```
   Major updates for production deployment:

   - ✅ Docker setup with multi-stage build
   - ✅ Railway.app configuration
   - ✅ Replace OpenRouter with direct API integrations (Claude, Gemini, OpenAI, Grok)
   - ✅ Comprehensive deployment documentation
   - ✅ Environment variable configuration

   Ready to deploy to Railway.app!
   ```

5. **Klicke auf "Create pull request"**

6. **Merge den PR** (klicke auf "Merge pull request")

7. **Dann in Railway:**
   - Deploy from GitHub
   - Wähle `7d3c/ai-counsel`
   - Railway wird automatisch den `master` Branch nutzen
   - Füge die Environment Variables hinzu

---

## Nach dem Merge

Sobald der PR gemerged ist, ist alles auf dem `master` Branch und Railway kann direkt deployen.
