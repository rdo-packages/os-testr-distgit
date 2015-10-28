%global pypi_name os-testr

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        0.4.1
Release:        1%{?dist}
Summary:        A testr wrapper to provide functionality for OpenStack projects

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

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
%setup -qc
mv %{pypi_name}-%{version} python2

pushd python2
rm -rf *.egg-info

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

cp -p LICENSE ChangeLog CONTRIBUTING.rst PKG-INFO README.rst ../
popd

%if 0%{?with_python3}
cp -a python2 python3
find python3 -name '*.py' | xargs sed -i 's|^#!/usr/bin/env python2|#!%{__python3}|'
%endif

find python2 -name '*.py' | xargs sed -i 's|^#!/usr/bin/env python2|#!%{__python2}|'

%build
pushd python2
%{__python2} setup.py build
popd
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd python3
%{__python3} setup.py install --skip-build --root=$RPM_BUILD_ROOT
for file in $RPM_BUILD_ROOT%{python3_sitelib}/os_testr/{subunit_trace,os_testr,subunit2html}.py;do
    chmod a+x $file
done
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build-3 -b html -d build/doctrees   source build/html

# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd
%endif

pushd python2
%{__python2} setup.py install --skip-build --root=$RPM_BUILD_ROOT
for file in $RPM_BUILD_ROOT%{python2_sitelib}/os_testr/{subunit_trace,os_testr,subunit2html}.py; do
    chmod a+x $file
done
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.buildinfo

# Fix this rpmlint warning
sed -i "s|\r||g" build/html/_static/jquery.js
popd
popd

%files
%doc README.rst
%license LICENSE
%{_bindir}/ostestr
%{_bindir}/subunit-trace
%{_bindir}/subunit2html
%{python2_sitelib}/os_testr
%{python2_sitelib}/os_testr-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/ostestr
%{_bindir}/subunit-trace
%{_bindir}/subunit2html
%{python3_sitelib}/os_testr
%{python3_sitelib}/os_testr-%{version}-py?.?.egg-info
%endif

%files doc
%license LICENSE
%doc python2/doc/build/html

%if 0%{?with_python3}
%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc python3/doc/build/html
%endif

%changelog
* Wed Oct 28 2015 Alan Pevec <alan.pevec@redhat.com> 0.4.1-1
- Update to 0.4.1

* Wed Aug 19 2015 chandankumar <chkumar246@gmail.com> - 0.3.0-1
- Initial package.
