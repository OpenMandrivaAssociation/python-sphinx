%define tarname	Sphinx
%define name	python-sphinx
%define version	0.6.1
%define release	%mkrel 1

Summary:	Python documentation generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{tarname}-%{version}.tar.gz
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	python-pygments >= 0.8, python-jinja2 >= 2.1
Requires:	python-docutils >= 0.4
Requires:	python-pkg-resources
BuildRequires:	python-setuptools
BuildRequires:	tetex-latex, python-docutils >= 0.4
BuildRequires:	python-jinja2 >= 2.1
%py_requires -d

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%prep
%setup -q -n %{tarname}-%{version}

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=FILELIST

make -C doc latex
make -C doc/_build/latex all-pdf

%clean
%__rm -rf %{buildroot}

%files -f FILELIST
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE TODO doc/_build/latex/sphinx.pdf
