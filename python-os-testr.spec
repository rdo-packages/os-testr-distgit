%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-testr

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        A testr wrapper to provide functionality for OpenStack projects

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/os-testr/os-testr-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

Requires:       python-pbr
Requires:       python-babel
Requires:       python-testrepository
Requires:       python-subunit
Requires:       python-testtools
Requires:       python-setuptools
Provides:       python2-os-testr

%description
ostestr is a testr wrapper that uses subunit-trace for output and builds
some helpful extra functionality around testr.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:       A testr wrapper to provide functionality for OpenStack projects
BuildArch:     noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools

Requires:       python3-pbr
Requires:       python3-babel
Requires:       python3-testrepository
Requires:       python3-subunit
Requires:       python3-testtools
Requires:       python3-setuptools

%description -n python3-%{pypi_name}
ostestr is a testr wrapper that uses subunit-trace for output and builds
some helpful extra functionality around testr.
%endif

%package doc
Summary: Documentation for ostestr module
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for ostestr module

%if 0%{?with_python3}
%package -n python3-%{pypi_name}-doc
Summary: Documentation for ostestr module
BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx

%description -n python3-%{pypi_name}-doc
Documentation for ostestr module
%endif


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# Fix this rpmlint warning
sed -i "s|\r||g" doc/build/html/_static/jquery.js

%install
%py2_install
for file in $RPM_BUILD_ROOT%{python2_sitelib}/os_testr/{subunit_trace,ostestr,subunit2html}.py; do
    chmod a+x $file
done
%if 0%{?with_python3}
%py3_install
for file in $RPM_BUILD_ROOT%{python3_sitelib}/os_testr/{subunit_trace,ostestr,subunit2html}.py;do
    chmod a+x $file
done
%endif

%files
%doc README.rst
%license LICENSE
%if ! 0%{?with_python3}
%{_bindir}/generate-subunit
%{_bindir}/ostestr
%{_bindir}/subunit-trace
%{_bindir}/subunit2html
%endif
%{python2_sitelib}/os_testr
%{python2_sitelib}/os_testr-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/generate-subunit
%{_bindir}/ostestr
%{_bindir}/subunit-trace
%{_bindir}/subunit2html
%{python3_sitelib}/os_testr
%{python3_sitelib}/os_testr-*.egg-info
%endif

%files doc
%license LICENSE
%doc doc/build/html

%changelog
