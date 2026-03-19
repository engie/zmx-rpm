%global zig_version 0.15.2

Name:           zmx
Version:        0.4.1
Release:        1%{?dist}
Summary:        Session persistence for terminal processes

License:        MIT
URL:            https://github.com/neurosnap/zmx
Source0:        %{url}/archive/v%{version}/zmx-%{version}.tar.gz

BuildRequires:  tar
BuildRequires:  git-core
BuildRequires:  glibc-devel

# Zig is not packaged in Fedora/EPEL, so we bootstrap it during build.
# The spec downloads a prebuilt Zig compiler for the build architecture.

# Zig produces statically-linked binaries without GNU build IDs
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}

%description
zmx provides session persistence for terminal processes. It lets you attach
and detach from shell sessions without killing them, restore terminal state
and output on re-attachment, and connect multiple clients to the same session.

Unlike tmux and screen, zmx does not provide windows, tabs, or splits —
it defers window management to your OS or terminal emulator.

%prep
%autosetup -n zmx-%{version}

# Download zig compiler for the build architecture
%ifarch x86_64
%global zig_arch x86_64
%endif
%ifarch aarch64
%global zig_arch aarch64
%endif

curl -sL "https://ziglang.org/download/%{zig_version}/zig-%{zig_arch}-linux-%{zig_version}.tar.xz" \
    -o zig.tar.xz
tar xf zig.tar.xz
mv zig-%{zig_arch}-linux-%{zig_version} zig-sdk

%build
# Initialize a git repo so build.zig can resolve git SHA
git init -q
git config user.email "build@localhost"
git config user.name "build"
git add -A && git commit -q -m "build"

./zig-sdk/zig build \
    -Doptimize=ReleaseSafe \
    -Dversion=%{version} \
    --prefix "zig-out"

%install
install -Dm755 zig-out/bin/zmx %{buildroot}%{_bindir}/zmx

# Generate and install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d

zig-out/bin/zmx completions bash > %{buildroot}%{_datadir}/bash-completion/completions/zmx
zig-out/bin/zmx completions zsh  > %{buildroot}%{_datadir}/zsh/site-functions/_zmx
zig-out/bin/zmx completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/zmx.fish

%files
%license LICENSE
%{_bindir}/zmx
%{_datadir}/bash-completion/completions/zmx
%{_datadir}/zsh/site-functions/_zmx
%{_datadir}/fish/vendor_completions.d/zmx.fish

%changelog
* Mon Feb 23 2026 Eric Bower <zmx@erickbower.com> - 0.4.1-1
- Fix zmx run stdin regression with ZMX_TASK_COMPLETED
- Fix zmx run DA response query when no client attached
- Fix zmx run re-quoting with shell meta chars
- Fix zmx wait use-after-free

* Fri Feb 13 2026 Eric Bower <zmx@erickbower.com> - 0.4.0-1
- Add zmx run for running commands in sessions
- Add zmx wait for waiting on sessions to complete
- Rename zmx send to zmx write
