Summary:	Tool to create isolated Python environments
Name:		python-virtualenv
Version:	1.3.3
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://pypi.python.org/packages/source/v/virtualenv/virtualenv-%{version}.tar.gz
# Source0-md5:	28e2955aed4ffc4dc3df02dc632b5c42
URL:		http://pypi.python.org/pypi/virtualenv
Requires:	python-setuptools
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
%{py_sitescriptdir}/virtualenv-%{version}-py*.egg-info
%{py_sitescriptdir}/virtualenv.py*
%attr(755,root,root) %{_bindir}/virtualenv
%exclude %{py_sitescriptdir}/rebuild-script.py*
%exclude %{py_sitescriptdir}/refresh-support-files.py*
%exclude %{py_sitescriptdir}/support-files
