#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# pytest tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Name:		python-virtualenv
Version:	16.0.0
Release:	4
License:	MIT
Group:		Development/Languages
#Source0Download: https://pypi.org/simple/virtualenv/
Source0:	https://files.pythonhosted.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	4feb74ee26255dd7e62e36ce96bcc4c6
Source1:	unpack-support.py
Patch0:		multilib.patch
Patch1:		rebuild-support.patch
URL:		https://pypi.org/project/virtualenv/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-modules >= 1:2.7.10-6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-modules >= 1:3.5.0-6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
# Blame binary-only python packages authors
# virtualenv wants *.py
Requires:	python-devel-src >= 1:2.7
# for virtualenv-2 wrapper
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%description -l pl.UTF-8
virtualenv to narzędzie do tworzenia oddzielonych środowisk Pythona.
Jest to następca workignenv i rozszerzenie virtual-pythona. Jest
tworzone przez Iana Bickinga i sponsorowane przez Open Planning
Project. Zostało wydane na liberalnej licencji w stylu MIT.

%package -n python3-%{module}
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4
# for virtualenv-3 wrapper
Requires:	python3-setuptools

%description -n python3-%{module}
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%description -n python3-%{module} -l pl.UTF-8
virtualenv to narzędzie do tworzenia oddzielonych środowisk Pythona.
Jest to następca workignenv i rozszerzenie virtual-pythona. Jest
tworzone przez Iana Bickinga i sponsorowane przez Open Planning
Project. Zostało wydane na liberalnej licencji w stylu MIT.

%package -n virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Group:		Libraries/Python
%if %{with python3}
Requires:	python3-virtualenv = %{version}-%{release}
%else
Requires:	python-virtualenv = %{version}-%{release}
%endif

%description -n virtualenv
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%description -n virtualenv -l pl.UTF-8
virtualenv to narzędzie do tworzenia oddzielonych środowisk Pythona.
Jest to następca workignenv i rozszerzenie virtual-pythona. Jest
tworzone przez Iana Bickinga i sponsorowane przez Open Planning
Project. Zostało wydane na liberalnej licencji w stylu MIT.

%prep
%setup -q -n virtualenv-%{version}
install -p %{SOURCE1} bin
%{__python} ./bin/unpack-support.py
%patch0 -p1
%patch1 -p1
%{__python} ./bin/rebuild-script.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs text
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
cp -p $RPM_BUILD_ROOT%{_bindir}/virtualenv{,-2}
%endif

%if %{with python3}
%py3_install
cp -p $RPM_BUILD_ROOT%{_bindir}/virtualenv{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst docs/_build/text/*.txt
%attr(755,root,root) %{_bindir}/virtualenv-2
%{py_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py_sitescriptdir}/virtualenv.py*
%dir %{py_sitescriptdir}/virtualenv_support
%{py_sitescriptdir}/virtualenv_support/*.py
%{py_sitescriptdir}/virtualenv_support/*.py[co]
%{py_sitescriptdir}/virtualenv_support/*.whl
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst docs/_build/text/*.txt
%attr(755,root,root) %{_bindir}/virtualenv-3
%{py3_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py3_sitescriptdir}/__pycache__/virtualenv*
%{py3_sitescriptdir}/virtualenv.py*
%dir %{py3_sitescriptdir}/virtualenv_support
%{py3_sitescriptdir}/virtualenv_support/*.py
%{py3_sitescriptdir}/virtualenv_support/*.whl
%{py3_sitescriptdir}/virtualenv_support/__pycache__
%endif

%files -n virtualenv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/virtualenv
