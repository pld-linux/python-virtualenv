Summary:	Tool to create isolated Python environments
Summary(pl.UTF-8):	Narzędzie do tworzenia oddzielonych środowisk Pythona
Name:		python-virtualenv
Version:	1.11.6
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	https://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	f61cdd983d2c4e6aeabb70b1060d6f49
Source1:	https://raw.github.com/pypa/virtualenv/%{version}/bin/rebuild-script.py
# Source1-md5:	5925c9a7d8e8b101c76b9c6cfa9ff297
Source2:	unpack-support.py
Patch0:		virtualenv-pld.patch
Patch1:		virtualenv-rebuild-support.patch
URL:		https://pypi.python.org/pypi/virtualenv
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm-pythonprov
Requires:	python-setuptools
# Blame binary-only python packages authors
# virtualenv wants *.py
Requires:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprov	'pythonegg\\(setuptools\\)'

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

%prep
%setup -q -n virtualenv-%{version}
%{__install} -d bin
%{__install} -m 755 -p %{SOURCE1} bin/
%{__install} -m 755 -p %{SOURCE2} bin/
%patch1 -p1

%{__python} ./bin/unpack-support.py

%patch0 -p1

%{__python} ./bin/rebuild-script.py

%build
%{__python} setup.py build

cd docs
%{__make} text

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# not needed
%{__rm} $RPM_BUILD_ROOT%{_bindir}/virtualenv-*.*
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/virtualenv_support/[ads]*.py{,[co]}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/_build/text/*.txt
%attr(755,root,root) %{_bindir}/virtualenv
%{py_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py_sitescriptdir}/virtualenv.py*
%dir %{py_sitescriptdir}/virtualenv_support
%{py_sitescriptdir}/virtualenv_support/__init__.py*
%{py_sitescriptdir}/virtualenv_support/*.whl
