# Maintainer: Leonard Anderweit <leonard.anderweit at gmail dot com>
pkgname=quadro-control-git
pkgver=0.1.0
pkgrel=1
pkgdesc="GUI control for Aquacomputer Quadro"
arch=('any')
url="https://github.com/leoratte/aquacomputer-quadro-control"
license=('GPL3')
groups=()
depends=('python3' 'python3-pyqt5' 'python-crccheck' 'python-pyusb')
makedepends=()
optdepends=()
provides=('quadro-control')
conflicts=()
source=("$pkgname::git+https://github.com/leoratte/aquacomputer-quadro-control.git:")
https://aur.archlinux.org/imhex-git.git
build() {
}

package() {
  cd "$pkgname-$pkgver"

  make DESTDIR="$pkgdir/" install
}