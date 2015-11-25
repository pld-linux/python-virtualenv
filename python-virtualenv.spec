#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do perform tests (does not work)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define module	virtualenv
Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Name:		python-virtualenv
Version:	12.0.4
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	https://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	ce7c4025516806b791bbd5b4ff6c4b84
Source2:	unpack-support.py
Patch0:		virtualenv-pld.patch
Patch1:		virtualenv-rebuild-support.patch
URL:		https://pypi.python.org/pypi/virtualenv
%if %{with python2}
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-setuptools
# Blame binary-only python packages authors
# virtualenv wants *.py
Requires:	python-devel-src
Suggests:	gcc
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
Requires:	python3-modules

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

%prep
%setup -q -n virtualenv-%{version}
install -p -p %{SOURCE2} bin
%patch1 -p1

%{__python} ./bin/unpack-support.py

%patch0 -p1

%{__python} ./bin/rebuild-script.py

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} text
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
%endif

%if %{with python2}
%py_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc docs/_build/text/*.txt
%attr(755,root,root) %{_bindir}/virtualenv
%attr(755,root,root) %{_bindir}/virtualenv-2.*
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

%doc docs/_build/text/*.txt
%if %{without python2}
%attr(755,root,root) %{_bindir}/virtualenv
%endif
%attr(755,root,root) %{_bindir}/virtualenv-3.*
%{py3_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py3_sitescriptdir}/__pycache__/virtualenv*
%{py3_sitescriptdir}/virtualenv.py*
%dir %{py3_sitescriptdir}/virtualenv_support
%{py3_sitescriptdir}/virtualenv_support/*.py
%{py3_sitescriptdir}/virtualenv_support/*.whl
%{py3_sitescriptdir}/virtualenv_support/__pycache__
%endif
