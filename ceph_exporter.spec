#
# spec file for package golang-github-digitalocean-ceph_exporter
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%{go_nostrip}

Name:           ceph_exporter
Version:        1.1.0+git20170818.80aa3ff
Release:        0
License:        Apache-2.0
Summary:        Prometheus exporter for ceph cluster metrics
Url:            https://github.com/digitalocean/ceph_exporter
Group:          System/Management
Source:         ceph_exporter-%{version}.tar.xz
Source1:        prometheus-ceph_exporter.service
BuildRequires:  fdupes
BuildRequires:  librados-devel
BuildRequires:  librbd-devel
BuildRequires:  golang-packaging
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%{?systemd_requires}
Requires(pre):  shadow
%{go_provides}

%description
Prometheus exporter that scrapes meta information about a running
ceph cluster.  All the information gathered from the cluster is done
by interacting with the monitors using an appropriate wrapper over
rados_mon_command(). Hence, no additional setup is necessary other
than having a working ceph cluster.

%prep
%setup -q -n ceph_exporter-%{version}

%build
%goprep github.com/digitalocean/ceph_exporter
%gobuild

%install
%goinstall
%gosrc
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/ceph_exporter.service
install -Dd -m 0755 %{buildroot}%{_sbindir}
ln -s /usr/sbin/service %{buildroot}%{_sbindir}/rcceph_exporter
%gofilelist
%fdupes %{buildroot}

%pre
%service_add_pre ceph_exporter.service
#getent group prometheus >/dev/null || %{_sbindir}/groupadd -r prometheus
#getent passwd prometheus >/dev/null || %{_sbindir}/useradd -r -g prometheus -d %{_localstatedir}/lib/prometheus -M -s /sbin/nologin prometheus

%post
%service_add_post ceph_exporter.service

%preun
%service_del_preun ceph_exporter.service

%postun
%service_del_postun ceph_exporter.service

%files -f file.lst
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/ceph_exporter
%{_unitdir}/ceph_exporter.service
%{_sbindir}/rcceph_exporter

%changelog

