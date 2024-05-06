# debuginfo doesn't work yet
%global debug_package %{nil}

Epoch: 2
Name: netavark
Version: 1.10.3
Release: 1%{?dist}
License: ASL 2.0 and BSD and MIT
ExclusiveArch: %{rust_arches}
# this is needed for go-md2man
# https://fedoraproject.org/wiki/PackagingDrafts/Go#Go_Language_Architectures
ExclusiveArch: %{go_arches}
ExcludeArch: i686
Summary: OCI network stack
URL: https://github.com/containers/%{name}
Source0: %{url}/archive/v%{version}/%{version}.tar.gz
Source1: %{url}/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
BuildRequires: cargo
BuildRequires: /usr/bin/go-md2man
Recommends: aardvark-dns >= 1.0.3
Provides: container-network-stack = 2
BuildRequires: make
BuildRequires: rust-srpm-macros
BuildRequires: systemd-rpm-macros
BuildRequires: git-core
BuildRequires: protobuf-compiler
BuildRequires: protobuf-c
BuildRequires: gcc

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
[source."git+https://github.com/namib-project/nftables-rs.git?rev=1b0c60b"]
git = "https://github.com/namib-project/nftables-rs.git"
rev = "1b0c60b"
replace-with = "vendored-sources"

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
go-md2man -in %{name}.1.md -out %{name}.1

%install
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%files
%license LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}
%{_unitdir}/*
%{_mandir}/man1/%{name}.1*

%changelog
* Mon Feb 12 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.3-1
- update to https://github.com/containers/netavark/releases/tag/v1.10.3
- Related: RHEL-2112

* Thu Feb 01 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.2-1
- update to https://github.com/containers/netavark/releases/tag/v1.10.2
- Related: RHEL-2112

* Thu Jan 25 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.1-1
- update to https://github.com/containers/netavark/releases/tag/v1.10.1
- Related: RHEL-2112

* Thu Jan 25 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.0-2
- Fix build of 1.10.0 - thanks to Lokesh Mandvekar
- Related: Jira:RHEL-2112

* Wed Jan 24 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.10.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.10.0
- Related: RHEL-2112

* Tue Dec 05 2023 Lokesh Mandvekar <lsm5@redhat.com> - 2:1.9.0-1
- require systemd srpm macros
- Related: Jira:RHEL-16291

* Fri Oct 06 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.8.0-3
- require systemd srpm macros
- Related: Jira:RHEL-2112

* Mon Oct 02 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.8.0-2
- fix directory for systemd units
- Related: Jira:RHEL-2112

* Fri Sep 29 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.8.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.8.0
- Related: Jira:RHEL-2112

* Mon Jul 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.7.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.7.0
- Related: #2176063

* Mon Jun 12 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.6.0-2
- rebuild
- Resolves: #2188340

* Wed Apr 12 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.6.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.6.0
- Related: #2176063

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-2
- fix build - thank to Paul Holzinger
- Related: #2124478

* Fri Feb 03 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.5.0
- Related: #2124478

* Thu Dec 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.4.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.4.0
- Related: #2124478

* Wed Nov 16 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.3.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.3.0
- Related: #2124478

* Tue Oct 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.2.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.2.0
- Related: #2124478

* Fri Aug 05 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-6
- add gating.yaml
- Related: #2061316

* Fri Aug 05 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-5
- properly disable i686
- Related: #2061316

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-4
- manually exclude i686 as build still fails
- Related: #2061316

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1.1.0-3
- set Epoch to preserve update path and build for go arches only
- Related: #2061316

* Thu Aug 04 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-2
- fix deps to go-md2man
- Related: #2061316

* Wed Aug 03 2022 Jindrich Novy <jnovy@redhat.com> - 1.1.0-1
- initial import
- Related: #2061316
