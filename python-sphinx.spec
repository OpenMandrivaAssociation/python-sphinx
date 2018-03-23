%define tarname	sphinx

# disable these for bootstrapping nose and sphinx
%bcond_with tests
%bcond_with doc

%define __noautoreq 'pythonegg\\(typing\\)'
%define upstreamver %(echo %{version} |sed -e 's,[~+],,')

Summary:	Python documentation generator
Name:		python-sphinx
Version:	1.7.1
Release:	2
Source0:	https://github.com/sphinx-doc/sphinx/archive/v%{upstreamver}.tar.gz
Source1000:	%{name}.rpmlintrc
#Patch0:	Sphinx-1.2.2-mantarget.patch
#Patch1:        Sphinx-1.2.2-babel-option.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx-doc.org/
BuildArch:	noarch
Requires:	python-pkg-resources
Requires:	python-docutils
Requires:	python-jinja2
Requires:	python-pygments
Requires:	python-sphinxcontrib-websupport
BuildRequires:	python-setuptools
%if %{with doc}
BuildRequires:	python-docutils >= 0.7
BuildRequires:	python-jinja2 >= 2.3
%endif
%if %{with tests}
BuildRequires:	python-nose
BuildRequires:	python-pygments
BuildRequires:  python-jinja2
%endif
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3-distribute
Obsoletes:	python2-sphinx < %{EVRD}
%rename python3-sphinx

%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%if %{with python2}
%package -n python2-sphinx
Summary:	Python documentation generator for Python 2.x
Group:		Development/Python
Requires:	python2-docutils >= 0.7
Requires:	python2-pygments >= 1.2
Requires:	python2-jinja2 >= 2.3
BuildRequires:	pkgconfig(python2)
BuildRequires:	python2-nose
BuildRequires:	python2-pygments
BuildRequires:  python2-jinja2
BuildRequires:	python2-setuptools

%description -n python2-sphinx
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.
%endif

%if %{with doc}
%package doc
Summary:	Documentation for %{name}

Group:		Development/Python
License:	BSD
Requires:	%{name} = %{EVRD}

%description doc
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package contains documentation in reST and HTML formats.
%endif

%prep
%setup -qn %{tarname}-%{upstreamver}
%apply_patches

%build
python setup.py build

%if %{with doc}
cd doc
make html man
rm -rf _build/html/.buildinfo
mv _build/html ..
%endif

%install
python setup.py install --skip-build --root=%{buildroot} 

%if %{with doc}
cd doc
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
mv _build/man/sphinx-*.1 %{buildroot}%{_mandir}/man1/
cd ..

# Deliver rst files
rm -rf doc/_build
sed -i 's|python ../sphinx-build.py|/usr/bin/sphinx-build|' doc/Makefile
mv doc reST
%endif

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{py_puresitedir}

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/__pycache__' -not -path '*/\.*' -printf "%f "`;
do
  install -d %{buildroot}%{_datadir}/sphinx/locale/$lang
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.js \
     %{buildroot}%{_datadir}/sphinx/locale/$lang/
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.mo \
    %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
  rm -rf sphinx/locale/$lang
done
popd

%find_lang sphinx

# Language files; Since these are javascript, it's not immediately obvious to
# find_lang that they need to be marked with a language.
(cd %{buildroot} && find . -name 'sphinx.js') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.js$\):%lang(\2) \1\2\3:' \
  >> sphinx.lang


%check
%if %{with tests}
make test
%endif

%files -f sphinx.lang
%doc AUTHORS CHANGES EXAMPLES LICENSE
%{_bindir}/sphinx-*
%{py_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%if %{with doc}
%{_mandir}/man1/*
%endif

%if %{with doc}
%files doc
%doc html reST
%endif
