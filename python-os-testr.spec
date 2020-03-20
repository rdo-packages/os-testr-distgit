# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-testr

%global with_doc 1

%global common_desc \
ostestr is a testr wrapper that uses subunit-trace for output and builds \
some helpful extra functionality around testr.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        A testr wrapper to provide functionality for OpenStack projects

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{pypi_name}
Source0:        https://tarballs.openstack.org/os-testr/os-testr-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary: %summary
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-babel
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-setuptools

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary: Documentation for ostestr module
BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for ostestr module
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}
for file in %{buildroot}%{pyver_sitelib}/os_testr/{subunit_trace,ostestr,subunit2html}.py; do
    chmod a+x $file
done

# Fix ambiguous shebangs for RHEL > 7 and Fedora > 29
%if %{pyver} == 3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/os_testr/
%endif

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/generate-subunit
%{_bindir}/ostestr
%{_bindir}/subunit-trace
%{_bindir}/subunit2html
%{pyver_sitelib}/os_testr
%{pyver_sitelib}/os_testr-*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
