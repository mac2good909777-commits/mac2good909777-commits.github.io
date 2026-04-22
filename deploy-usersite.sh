#!/bin/bash
# 推到 user-site repo：mac2good909777-commits.github.io (無子路徑)
set -e

USER_REPO="mac2good909777-commits.github.io"
OWNER="mac2good909777-commits"

cd "$(dirname "$0")"

echo "━━━ 1. Build 驗證（無 base）━━━"
npm run build 2>&1 | tail -3
[ -d dist ] || { echo "✗ build 失敗"; exit 1; }

echo ""
echo "━━━ 2. 切換 remote 到 user-site repo ━━━"
if ! gh repo view "$OWNER/$USER_REPO" >/dev/null 2>&1; then
  echo "建立 user-site repo：$USER_REPO"
  gh repo create "$OWNER/$USER_REPO" --public --description="張現傑 x 睦聚地產 — 工業不動產市場觀察平台" --confirm 2>/dev/null || \
    gh repo create "$OWNER/$USER_REPO" --public --description="張現傑 x 睦聚地產 — 工業不動產市場觀察平台"
fi

git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/$USER_REPO.git"

echo ""
echo "━━━ 3. Commit + push ━━━"
git add -A
git diff --cached --quiet && echo "(無新變更)" || git commit -m "Deploy to user-site repo (無子路徑部署)

- 從 project repo 移到 user-site repo
- 拿掉 astro.config.mjs 的 base 設定
- 所有絕對路徑 /about/、/market-view/ 等現在可正確運作

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"
git push -u origin main --force

echo ""
echo "━━━ 4. 啟用 Pages (workflow) ━━━"
gh api --method POST "repos/$OWNER/$USER_REPO/pages" -f "build_type=workflow" 2>&1 | head -3 || true

echo ""
echo "━━━ 5. 檢查 Actions ━━━"
sleep 3
gh run list --repo "$OWNER/$USER_REPO" --limit 1 2>&1 | head -3

echo ""
echo "━━━ Done ━━━"
echo "Repo:    https://github.com/$OWNER/$USER_REPO"
echo "Actions: https://github.com/$OWNER/$USER_REPO/actions"
echo "Live:    https://$USER_REPO/   (~1 分鐘後上線，無子路徑)"
