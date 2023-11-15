# debuginfo doesn't work yet
%global debug_package %{nil}

Epoch: 2
Name: netavark
Version: 1.7.0
Release: 1%{?dist}
License: ASL 2.0 and BSD and MIT
ExclusiveArch: %{rust_arches}
Summary: OCI network stack
URL: https://github.com/containers/%{name}
Source0: %{url}/archive/v%{version}/%{version}.tar.gz
Source1: %{url}/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
Source2: netavark.1
BuildRequires: cargo
Recommends: aardvark-dns >= 1.0.3
Provides: container-network-stack = 2
BuildRequires: make
BuildRequires: rust-srpm-macros
BuildRequires: git-core
BuildRequires: protobuf-compiler
BuildRequires: protobuf-c
BuildRequires: gcc
# https://github.com/containers/netavark/issues/578
ExcludeArch: i686

%description
%{summary}

Netavark is a rust based network stack for containers. It is being
designed to work with Podman but is also applicable for other OCI
container management applications.

Netavark is a tool for configuring networking for Linux containers.
Its features include:
* Configuration of container networks via JSON configuration file
* Creation and management of required network interfaces,
    including MACVLAN networks
* All required firewall configuration to perform NAT and port
    forwarding as required for containers
* Support for iptables and firewalld at present, with support
    for nftables planned in a future release
* Support for rootless containers
* Support for IPv4 and IPv6
* Support for container DNS resolution via aardvark-dns.

%prep
%autosetup -Sgit
tar fx %{SOURCE1}
mkdir -p .cargo

cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[net]
offline = true

[source."https://github.com/containers/netavark-dhcp-proxy"]
git = "https://github.com/containers/netavark-dhcp-proxy"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
%{__make} build

cd docs
cp %{SOURCE2} .

%install
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%files
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}
/usr/lib/systemd/system/*
%{_mandir}/man1/%{name}.1*

%changelog
* Mon Jul 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.7.0
- Related: #2176055

* Mon May 22 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.6.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.6.0
- Related: #2176055

* Thu Apr 20 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-5
- fix --dns-add command is not functioning
- Resolves: #2182897

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-4
- exclude i686
- Related: #2123641

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-3
- update build parameters
- Related: #2123641

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-2
- always stay offline during build
- Related: #2123641

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.5.0
- Related: #2123641

* Thu Dec 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.4.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.4.0
- Related: #2123641

* Mon Nov 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.3.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.3.0
- Related: #2123641

* Wed Sep 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.2.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.2.0
- Resolves: #2116481

* Tue Aug 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-6
- bump Epoch to preserve upgrade path
- Related: #2061390

* Tue Aug 09 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-5
- remove dependency on md2man
- Related: #2061390

* Tue Aug 09 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-4
- fix arches
- Related: #2061390

* Tue Aug 09 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-3
- add gating.yaml
- Related: #2061390

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-2
- require /usr/bin/go-md2man directly

* Wed Aug 03 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-1
- initial import
- Related: #2061390
