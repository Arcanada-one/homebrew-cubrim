class Cubrim < Formula
  desc "N-dimensional-cube lossless compressor and .cbr archiver"
  homepage "https://cubrim.com"
  version "0.3.2"
  license :cannot_represent

  on_macos do
    on_arm do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.3.2/cubrim-v0.3.2-macos-apple-silicon.tar.gz"
      sha256 "06479068d5903d545d8c16899e8a25e339ba85ded91bed874f299d28a2033782"
    end

    on_intel do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.3.2/cubrim-v0.3.2-macos-intel.tar.gz"
      sha256 "93810064ff54a1a8a4757a5a09322a9ab4b8d1183d0bed254df364f11513f60a"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.3.2/cubrim-v0.3.2-linux-arm64.tar.gz"
      sha256 "990a3d091b2de60af2039da42e17d3f5696202dd7545f9ddf16ae7c6b213933a"
    end

    on_intel do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.3.2/cubrim-v0.3.2-linux-x86_64.tar.gz"
      sha256 "cbf672e15e425032b6b9bcf28c1308650edb9b4de47d6e04a26414a038ed36fe"
    end
  end

  def install
    bin.install "cubrim"
  end

  test do
    assert_match "cubrim", shell_output("#{bin}/cubrim --version")
  end
end
