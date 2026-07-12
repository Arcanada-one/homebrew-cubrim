class Cubrim < Formula
  desc "N-dimensional-cube lossless compressor and .cbr archiver"
  homepage "https://cubrim.com"
  version "0.1.0-cubr0043"
  license :cannot_represent

  on_macos do
    on_arm do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.1.0-cubr0043/cubrim-v0.1.0-cubr0043-macos-apple-silicon.tar.gz"
      sha256 "6df8d18e7895b3011a419a42d89f7d30ddcc19b2eb232dedfa40972cfb03bc57"
    end

    on_intel do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.1.0-cubr0043/cubrim-v0.1.0-cubr0043-macos-intel.tar.gz"
      sha256 "6683b06f60c9f1d9063010d35a0c41bc22768947d840f5b90bb6d9d92de2da05"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.1.0-cubr0043/cubrim-v0.1.0-cubr0043-linux-arm64.tar.gz"
      sha256 "94a4367802c97c664e286b7bc7e1d9d3d100eb401930be59435fb4ab3cede048"
    end

    on_intel do
      url "https://github.com/Arcanada-one/cubrim/releases/download/v0.1.0-cubr0043/cubrim-v0.1.0-cubr0043-linux-x86_64.tar.gz"
      sha256 "e2bc786298d5cea0c578109fc548c987a6a73c85453c76f2c61c087b368c20d9"
    end
  end

  def install
    bin.install "cubrim"
  end

  test do
    assert_match "cubrim", shell_output("#{bin}/cubrim --version")
  end
end
