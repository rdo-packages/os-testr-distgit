%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-testr

%if 0%{?fedora}|| 0%{?rhel} > 7
%global with_python3 1
%endif

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

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary: %summary

Requires:       python2-pbr
Requires:       python2-babel
Requires:       python2-stestr
Requires:       python2-subunit
Requires:       python2-testtools
Requires:       python2-setuptools
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:       A testr wrapper to provide functionality for OpenStack projects
BuildArch:     noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  /usr/bin/pathfix.py

Requires:       python3-pbr
Requires:       python3-babel
Requires:       python3-stestr
Requires:       python3-subunit
Requires:       python3-testtools
Requires:       python3-setuptools

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package doc
Summary: Documentation for ostestr module
BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description doc
Documentation for ostestr module
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# Fix this rpmlint warning
sed -i "s|\r||g" doc/build/html/_static/jquery.js
%endif

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

# Fix ambiguous shebangs for RHEL > 7 and Fedora > 29
%if 0%{?with_python3}
pathfix.py -pni "%{__python2} %{py2_shbang_opts}" %{buildroot}%{python2_sitelib}/os_testr/
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/os_testr/
%endif

%files -n python2-%{pypi_name}
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

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
