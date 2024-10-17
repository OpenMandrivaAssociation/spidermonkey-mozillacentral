%define _requires_exceptions devel(libnspr4\\|devel(libplc4\\|devel(libplds4

%define	major	1
%define _suffix		central
%define jsname		js%{_suffix}
%define mozjsname	moz%{jsname}
%define jsnamestatic	%{jsname}_static
%define	libname	%mklibname %{mozjsname}_ %{major}
%define	devname	%mklibname %{mozjsname} -d

Summary:	SpiderMonkey, the Mozilla JavaScript engine (mozilla-%{_suffix} Edition)
Name:		spidermonkey-mozilla%{_suffix}
## Version comes from $ hg log -l 1 --template '0.hg{rev}.{latesttag}.{node|short}\n'
Version:	0.hg75545.AURORA_BASE_20110816.77bc1868ea23
Release:	1
License:	MPL
Group:		Development/Other
URL:		https://www.mozilla.org/js/
## Generated from mozilla-central mercurial repository, with:
## $ hg archive --prefix spidermonkey-mozillacentral-$(hg log -l 1 --template '0.hg{rev}.{latesttag}.{node|short}')/ \
## --include "js/src/" --include "mfbt/" \
## spidermonkey-mozillacentral-$(hg log -l 1 --template '0.hg{rev}.{latesttag}.{node|short}').tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	nspr-devel
BuildRequires:	readline-devel
BuildRequires:	autoconf2.1
BuildRequires:	python
# wtf?
BuildRequires:	zip

%description
The JavaScript engine compiles and executes scripts containing JavaScript
statements and functions. The engine handles memory allocation for the
objects needed to execute scripts, and it cleans up—garbage
collects—objects it no longer needs.

SpiderMonkey supports versions 1.0 through 1.8 of the JavaScript language.
JS 1.3 and later conform to the ECMAScript specification, ECMA 262-3.
Later versions also contain Mozilla extensions such as array comprehensions
and generators. SpiderMonkey also supports E4X (optionally).

Main purpose of this package is to be able to build Firefox with
Dehydra/Treehydra which requires quite recent versions of SpiderMonkey.

%package -n	%{libname}
Summary:	JavaScript engine library
Group:		System/Libraries

%description -n	%{libname}
The JavaScript engine compiles and executes scripts containing JavaScript
statements and functions. The engine handles memory allocation for the
objects needed to execute scripts, and it cleans up—garbage
collects—objects it no longer needs.

SpiderMonkey supports versions 1.0 through 1.8 of the JavaScript language.
JS 1.3 and later conform to the ECMAScript specification, ECMA 262-3.
Later versions also contain Mozilla extensions such as array comprehensions
and generators. SpiderMonkey also supports E4X (optionally).

Main purpose of this package is to be able to build Firefox with
Dehydra/Treehydra which requires quite recent versions of SpiderMonkey.

%package -n	%{devname}
Summary:	The header files for %{libname}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Requires:	nspr-devel

%description -n	%{devname}
These are the header files for development with SpiderMonkey.

Main purpose of this package is to be able to build Firefox with
Dehydra/Treehydra which requires quite recent versions of SpiderMonkey.

%prep
%setup -q -n %{name}-%{version}/js/src

# Renaming mozjs/js_static to mozjscentral/jscentral_static
# to avoid clashes
for source in $(find . -type f -name "*.in"); do
sed -ri 						\
	-e "s|mozjs|%{mozjsname}|g"			\
	-e "s|js_static|%{jsnamestatic}|g"		\
	-e "s|MODULE.*= js|MODULE = %{jsname}|g"	\
	$source;
done;

sed -ri				\
	-e "s|/js|/%{jsname}|g"	\
	js-config.in

autoconf-2.13

%build

%configure2_5x	--enable-readline \
		--enable-threadsafe \
		--enable-ctypes \
		--with-system-nspr
# \
#		--enable-debug \
#		--enable-debugger-info-modules \
#		--enable-debug-symbols

%make

%install
%makeinstall_std

chmod 644 %{buildroot}%{_includedir}/%{jsname}/*

# install binary
%{__install} -m755 shell/js -D %{buildroot}%{_bindir}/%{jsname}
%{__install} -m755 jscpucfg -D %{buildroot}%{_bindir}/%{jsname}cpucfg

%{__mv} %{buildroot}%{_bindir}/js-config %{buildroot}%{_bindir}/%{jsname}-config 

%multiarch_includes %{buildroot}%{_includedir}/%{jsname}/jsautocfg.h

cd ../../
pushd mfbt
for include in *.h; do
	%{__install} -m0644 -D $include %{buildroot}%{_includedir}/%{jsname}/mozilla/$include
done;
popd

%files
%{_bindir}/*

%files -n %{libname}
%{_libdir}/lib%{mozjsname}.so*

%files -n %{devname}
%doc README.html
%dir %{_includedir}/%{jsname}
%{multiarch_includedir}/%{jsname}/jsautocfg.h
%{_includedir}/%{jsname}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.desc
