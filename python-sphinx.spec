%define tarname	Sphinx
%define name	python-sphinx
%define version	1.0.4
%define release	%mkrel 2

Summary:	Python documentation generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://pypi.python.org/packages/source/S/%{tarname}/%{tarname}-%{version}.tar.gz
Patch0:         Sphinx-1.0b1-sagemath.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils >= 0.5
Requires:	python-pygments >= 0.8
Requires:	python-jinja2 >= 2.2
BuildRequires:	python-setuptools
BuildRequires:	python-docutils >= 0.5
Requires:	python-pygments >= 0.8
BuildRequires:	python-jinja2 >= 2.2
BuildRequires:	python-nose
%py_requires -d

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p1

%install
%__rm -rf %{buildroot}
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot} --record=FILE_LIST

%__make -C doc html

%clean
%__rm -rf %{buildroot}

%check
pushd tests
%__python run.py
popd

%files -f FILE_LIST
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE TODO doc/_build/html/
