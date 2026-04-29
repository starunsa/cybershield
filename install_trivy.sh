#!/usr/bin/env sh
set -eu

VERSION="${TRIVY_VERSION:-0.69.3}"
ARCH="$(uname -m)"

case "$ARCH" in
  arm64|aarch64)
    TRIVY_ARCH="ARM64"
    ;;
  x86_64|amd64)
    TRIVY_ARCH="64bit"
    ;;
  *)
    echo "Unsupported architecture: $ARCH" >&2
    exit 1
    ;;
esac

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
BIN_DIR="$ROOT_DIR/.bin"
TMP_DIR="$(mktemp -d)"
ARCHIVE="trivy_${VERSION}_macOS-${TRIVY_ARCH}.tar.gz"
URL="https://github.com/aquasecurity/trivy/releases/download/v${VERSION}/${ARCHIVE}"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$BIN_DIR"
echo "Downloading Trivy v${VERSION} from $URL"
curl -fL "$URL" -o "$TMP_DIR/$ARCHIVE"
tar -xzf "$TMP_DIR/$ARCHIVE" -C "$TMP_DIR" trivy
chmod +x "$TMP_DIR/trivy"
mv "$TMP_DIR/trivy" "$BIN_DIR/trivy"

echo "Installed Trivy to $BIN_DIR/trivy"
"$BIN_DIR/trivy" --version
