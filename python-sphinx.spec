%define tarname	Sphinx

# disable these for bootstrapping nose and sphinx
%define enable_tests 1
%define enable_doc 1

Summary:	Python documentation generator
Name:		python-sphinx
Version:	1.1.3
Release:	8
License:	BSD
Group:		Development/Python
Url:	http://sphinx.pocoo.org/
Source0:	http://pypi.python.org/packages/source/S/%{tarname}/%{tarname}-%{version}.tar.gz
Patch0:	Sphinx-1.1.3-sagemath.patch
Patch1:	Sphinx-1.1.3-fix_quoting_in_inheritance.patch
BuildArch:	noarch
BuildRequires:	python-setuptools
%if %enable_doc
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %enable_tests
BuildRequires:	python-nose
%endif
Requires:	python-docutils >= 0.7
Requires:	python-jinja2 >= 2.3
Requires:	python-pkg-resources
Requires:	python-pygments >= 1.2
%py_requires -d

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%prep
%setup -qn %{tarname}-%{version}
%apply_patches

%install
PYTHONDONTWRITEBYTECODE= %__python setup.py install --root=%{buildroot}
%if %enable_doc
%make -C doc html
%endif

%check
%if %enable_tests
pushd tests
%__python run.py
popd
%endif

%files
%doc AUTHORS CHANGES LICENSE TODO 
%if %enable_doc
%doc doc/_build/html/
%endif
%{_bindir}/sphinx*
%{py_sitedir}/sphinx/
%{py_sitedir}/Sphinx-*egg-info/

