# Building from fedora dependencies not possible
# Latest upstream rtnetlink frequently required
# sha2, zbus, zvariant are currently out of date

%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

# Minimum X.Y dep for aardvark-dns
%define major_minor %((v=%{version}; echo ${v%.*}))

# Set default firewall to nftables on CentOS Stream 10+, RHEL 10+, Fedora 41+
# and default to iptables on all other environments
# The `rhel` macro is defined on CentOS Stream, RHEL as well as Fedora ELN.
%if (%{defined rhel} && 0%{?rhel} >= 10) || (%{defined fedora} && 0%{?fedora} >= 41)
%define default_fw nftables
%else
%define default_fw iptables
%endif

Name: netavark
# Set a different Epoch for copr builds
%if %{defined copr_username}
Epoch: 102
%else
Epoch: 2
%endif
Version: 1.16.0
Release: 1%{?dist}
# The `AND` needs to be uppercase in the License for SPDX compatibility
License: Apache-2.0 AND BSD-3-Clause AND MIT
%if %{defined golang_arches_future}
ExclusiveArch: %{golang_arches_future}
%else
ExclusiveArch: aarch64 ppc64le s390x x86_64
%endif
Summary: OCI network stack
URL: https://github.com/containers/%{name}
# Tarballs fetched from upstream's release page
Source0: %{url}/archive/v%{version}.tar.gz
Source1: %{url}/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
BuildRequires: cargo
BuildRequires: %{_bindir}/go-md2man
# aardvark-dns and %%{name} are usually released in sync
Requires: aardvark-dns >=  %{epoch}:%{major_minor}
Provides: container-network-stack = 2
%if "%{default_fw}" == "nftables"
Requires: nftables
%else
Requires: iptables
%endif
BuildRequires: make
BuildRequires: protobuf-c
BuildRequires: protobuf-compiler
%if %{defined rhel}
# rust-toolset requires the `local` repo enabled on non-koji ELN build environments
BuildRequires: rust-toolset
%else
BuildRequires: rust-packaging
BuildRequires: rust-srpm-macros
%endif
BuildRequires: git-core
BuildRequires: systemd
BuildRequires: systemd-devel

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
* Support for iptables, firewalld and nftables
* Support for rootless containers
* Support for IPv4 and IPv6
* Support for container DNS resolution via aardvark-dns.

%prep
%autosetup -Sgit %{name}-%{version}
# Following steps are only required on environments like koji which have no
# network access and thus depend on the vendored tarball. Copr pulls
# dependencies directly from the network.
%if !%{defined copr_username}
tar fx %{SOURCE1}
%if 0%{?fedora} || 0%{?rhel} >= 10
%cargo_prep -v vendor
%else
%cargo_prep -V 1
%endif
%endif

%build
NETAVARK_DEFAULT_FW=%{default_fw} %{__make} CARGO="%{__cargo}" build
%if (0%{?fedora} || 0%{?rhel} >= 10) && !%{defined copr_username}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest
%endif

cd docs
%{__make}

%install
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install

%preun
%systemd_preun %{name}-dhcp-proxy.service
%systemd_preun %{name}-firewalld-reload.service

%postun
%systemd_postun %{name}-dhcp-proxy.service
%systemd_postun %{name}-firewalld-reload.service

%files
%license LICENSE
%if (0%{?fedora} || 0%{?rhel} >= 10) && !%{defined copr_username}
%license LICENSE.dependencies
%license cargo-vendor.txt
%endif
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/%{name}*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/%{name}-firewalld.7*
%{_unitdir}/%{name}-dhcp-proxy.service
%{_unitdir}/%{name}-dhcp-proxy.socket
%{_unitdir}/%{name}-firewalld-reload.service

%changelog
* Fri Aug 15 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.16.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.16.0
- Related: RHEL-80816

* Tue Jun 10 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.15.2-1
- update to https://github.com/containers/netavark/releases/tag/v1.15.2
- Related: RHEL-80816

* Mon Jun 02 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.15.1-1
- update to https://github.com/containers/netavark/releases/tag/v1.15.1
- Related: RHEL-80816

* Wed May 14 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.15.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.15.0
- Related: RHEL-80816

* Thu Mar 20 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.14.1-1
- update to https://github.com/containers/netavark/releases/tag/v1.14.1
- Related: RHEL-80816

* Mon Feb 10 2025 Jindrich Novy <jnovy@redhat.com> - 2:1.14.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.14.0
- Related: RHEL-60277

* Fri Dec 06 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.13.1-1
- update to https://github.com/containers/netavark/releases/tag/v1.13.1
- Related: RHEL-60277

* Wed Oct 30 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.13.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.13.0
- Resolves: RHEL-65326

* Tue Aug 20 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.12.2-1
- update to https://github.com/containers/netavark/releases/tag/v1.12.2
- Related: RHEL-27608

* Mon Aug 05 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.12.1-1
- update to https://github.com/containers/netavark/releases/tag/v1.12.1
- Related: RHEL-27608

* Mon Jun 03 2024 Jindrich Novy <jnovy@redhat.com> - 2:1.11.0-1
- update to https://github.com/containers/netavark/releases/tag/v1.11.0
- Related: RHEL-27608

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
