%define tarname	Sphinx
%define name	python-sphinx
%define version	1.1.1
%define release	%mkrel 1

# disable these for bootstrapping nose and sphinx
%define enable_tests 1
%define enable_doc 1

Summary:	Python documentation generator
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://pypi.python.org/packages/source/S/%{tarname}/%{tarname}-%{version}.tar.gz
Patch0:         Sphinx-1.1-sagemath.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils >= 0.7
Requires:	python-pygments >= 1.2
Requires:	python-jinja2 >= 2.3
BuildRequires:	python-setuptools
Requires:	python-pygments >= 1.2
%if %enable_doc
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %enable_tests
BuildRequires:	python-nose
%endif
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
%if %enable_doc
%__make -C doc html
%endif
%clean
%__rm -rf %{buildroot}

%check
%if %enable_tests
pushd tests
%__python run.py
popd
%endif

%files -f FILE_LIST
%defattr(-,root,root)
%doc AUTHORS CHANGES LICENSE TODO 
%if %enable_doc
%doc doc/_build/html/
%endif
