# debuginfo doesn't work yet
%global debug_package %{nil}

#%%global branch v1.5.0-rhel
%global commit0 8a6d81c51b2a130a3c93d94587df81053e208e05
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Epoch: 2
Name: netavark
Version: 1.5.1
Release: 2%{?dist}
License: ASL 2.0 and BSD and MIT
ExclusiveArch: %{rust_arches}
Summary: OCI network stack
URL: https://github.com/containers/%{name}
%if 0%{?branch:1}
Source0: https://github.com/containers/%{name}/tarball/%{commit0}/%{branch}-%{shortcommit0}.tar.gz
%else
Source0: https://github.com/containers/%{name}/archive/%{commit0}/%{name}-%{version}-%{shortcommit0}.tar.gz
%endif
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
%if 0%{?branch:1}
%autosetup -Sgit -n containers-%{name}-%{shortcommit0}
%else
%autosetup -Sgit -n %{name}-%{commit0}
%endif
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
%{_mandir}/man1/%{name}.1*

%changelog
* Wed Jun 07 2023 Jindrich Novy <jnovy@redhat.com> - 2:1.5.1-2
- update to 1.5.1 bugfix release
- Resolves: #2211989

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
