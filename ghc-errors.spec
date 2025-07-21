#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	errors
Summary:	Haskell errors library: Simplified error-handling
Summary(pl.UTF-8):	Biblioteka errors dla Haskella - uproszczona obsługa błędów
Name:		ghc-%{pkgname}
Version:	2.3.0
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/errors
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	43bec23a661dd4a5eefb5549b4fad8a8
URL:		http://hackage.haskell.org/package/errors
BuildRequires:	ghc >= 7.8.1
BuildRequires:	ghc-base >= 4.7
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-exceptions >= 0.6
BuildRequires:	ghc-exceptions < 0.11
BuildRequires:	ghc-safe >= 0.3.3
BuildRequires:	ghc-safe < 0.4
BuildRequires:	ghc-text < 1.3
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers < 0.6
BuildRequires:	ghc-transformers-compat >= 0.4
BuildRequires:	ghc-transformers-compat < 0.7
%if %{with prof}
BuildRequires:	ghc-prof >= 7.8.1
BuildRequires:	ghc-base-prof >= 4.7
BuildRequires:	ghc-exceptions-prof >= 0.6
BuildRequires:	ghc-safe-prof >= 0.3.3
BuildRequires:	ghc-text-prof
BuildRequires:	ghc-transformers-prof >= 0.2
BuildRequires:	ghc-transformers-compat-prof >= 0.4
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.7
Requires:	ghc-exceptions >= 0.6
Requires:	ghc-safe >= 0.3.3
Requires:	ghc-text
Requires:	ghc-transformers >= 0.2
Requires:	ghc-transformers-compat >= 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
The one-stop shop for all your error-handling needs! Just import
Control.Error.

This library encourages an error-handling style that directly uses
the type system, rather than out-of-band exceptions.

%description -l pl.UTF-8
Jeden produkt, spełniający wszystkie potrzeby obsługi błędów!
Wystarczy zaimportować Control.Error.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.7
Requires:	ghc-exceptions-prof >= 0.6
Requires:	ghc-safe-prof >= 0.3.3
Requires:	ghc-text-prof
Requires:	ghc-transformers-prof >= 0.2
Requires:	ghc-transformers-compat-prof >= 0.4

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Error
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Error/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Error/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Control/Error/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%endif
