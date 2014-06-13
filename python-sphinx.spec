%define tarname	Sphinx

# disable these for bootstrapping nose and sphinx
%define enable_tests 0
%define enable_doc 1
%define enable_python3 0

Summary:	Python documentation generator

Name:		python-sphinx
Version:	1.2.2 
Release:	3
Source0:	http://pypi.python.org/packages/source/S/%{tarname}/%{tarname}-%{version}.tar.gz
Patch0:	        Sphinx-1.2.2-mantarget.patch
Patch1:         Sphinx-1.2.2-babel-option.patch
License:	BSD
Group:		Development/Python
Url:		http://sphinx.pocoo.org/
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
BuildRequires:	python3-nose
BuildRequires:	python-pygments
BuildRequires:	python3-pygments
BuildRequires:  python-jinja2
BuildRequires:  python3-jinja2
%endif
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3-distribute


%description
Sphinx is a tool that facilitates the creation of beautiful
documentation for Python projects from reStructuredText sources. It
was originally created to format the new documentation for Python, but
has since been cleaned up in the hope that it will be useful in many
other projects.

%if %enable_python3
%package -n python3-sphinx
Summary:	Python documentation generator

Group:		Development/Python
Requires:	python3-docutils
Requires:	python3-jinja2
Requires:	python3-pygments

%description -n python3-sphinx
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.
%endif

%if %enable_doc
%package doc
Summary:	Documentation for %{name}

Group:		Development/Python
License:	BSD
Requires:	%{name} = %{version}-%{release}

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
%setup -qc
tar xzf %{SOURCE0}

mv %{tarname}-%{version} python2

pushd python2
%patch0 -p1 -b .mantarget
%patch1 -p1 -b .babel
sed '1d' -i sphinx/pycode/pgen2/token.py
popd

cp -r python2 python3

%build
pushd python2
python setup.py build
popd

%if %enable_python3
pushd python3
%{__python3} setup.py build
popd
%endif

%if %enable_doc
pushd python2
pushd doc
make html
make man
rm -rf _build/html/.buildinfo
mv _build/html ..
popd
popd
%endif


%install
%if %enable_python3
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
for f in %{buildroot}%{_bindir}/sphinx-*;
do
 mv $f $f-%{python3_version}
done
popd
%endif

pushd python2
python setup.py install --skip-build --root=%{buildroot} 

%if %enable_doc
pushd doc
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
mv _build/man/sphinx-*.1 %{buildroot}%{_mandir}/man1/
for f in %{buildroot}%{_mandir}/man1/sphinx-*.1;
do
    cp -p $f $(echo $f | sed -e "s|.1$|-%{python3_version}.1|")
done
popd

# Deliver rst files
rm -rf doc/_build
sed -i 's|python ../sphinx-build.py|/usr/bin/sphinx-build|' doc/Makefile
mv doc reST
%endif
popd

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{py_puresitedir}

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -printf "%f "`;
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
%if %enable_tests
pushd python2
pushd tests
%__python run.py
popd
popd
pushd python3
make test
popd
%endif

%files -f sphinx.lang
%doc python2/AUTHORS python2/CHANGES python2/EXAMPLES python2/LICENSE
%{_bindir}/sphinx-*
%{py_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%{_mandir}/man1/*
%if %enable_python3
%exclude %{_bindir}/sphinx-*-%{python3_version}
%exclude %{py3_puresitedir}/*
%exclude %{_mandir}/man1/sphinx-*-%{python3_version}.1*
%endif

%if %enable_python3
%files -n python3-sphinx
%doc python3/AUTHORS python3/CHANGES python3/EXAMPLES python3/LICENSE
%{_bindir}/sphinx-*-%{python3_version}
%{py3_puresitedir}/*
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%{_mandir}/man1/sphinx-*-%{python3_version}.1*
%endif

%if %enable_doc
%files doc
%doc python2/html python2/reST
%endif
