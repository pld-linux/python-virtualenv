Summary:	Tool to create isolated Python environments
Name:		python-virtualenv
Version:	1.6.4
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	1072b66d53c24e019a8f1304ac9d9fc5
Source1:	https://raw.github.com/pypa/virtualenv/%{version}/bin/rebuild-script.py
# Source1-md5:	b9748dcf1c81dc85a8368dcb7c680494
Source2:	unpack-support.py
URL:		http://pypi.python.org/pypi/virtualenv
Patch0:		virtualenv-pld.patch
BuildRequires:	python
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
Requires:	python-setuptools
# Blame binary-only python packages authors
# virtualenv wants *.py
Requires:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
virtualenv is a tool to create isolated Python environments.
virtualenv is a successor to workingenv, and an extension of
virtual-python. It is written by Ian Bicking, and sponsored by the
Open Planning Project. It is licensed under an MIT-style permissive
license.

%prep
%setup -q -n virtualenv-%{version}
%{__install} -d bin
%{__install} -m 755 -p %{SOURCE1} bin/
%{__install} -m 755 -p %{SOURCE2} bin/

python ./bin/unpack-support.py

%patch0 -p1

python ./bin/rebuild-script.py

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/index.txt
%attr(755,root,root) %{_bindir}/virtualenv
%{py_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py_sitescriptdir}/virtualenv.py*
%dir %{py_sitescriptdir}/virtualenv_support
%{py_sitescriptdir}/virtualenv_support/__init__.py*
%{py_sitescriptdir}/virtualenv_support/*.gz
