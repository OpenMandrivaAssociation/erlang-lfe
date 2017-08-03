%global realname lfe
%global upstream rvirding

# Set this to true when starting a rebuild of the whole erlang stack. There's a
# cyclical dependency between erlang-erts, erlang-lfe, and erlang-rebar so this
# package (erlang-lfe) needs to get built first in bootstrap mode.
%global need_bootstrap 1


%if 0%{?need_bootstrap}
%global _erllibdir %{_libdir}/erlang/lib
%global debug_package %{nil}
%endif


Name:		erlang-%{realname}
Version:	1.0.2
Release:	%mkrel 3
Summary:	Lisp Flavoured Erlang
Group:		Development/Erlang
License:	BSD
URL:		https://github.com/%{upstream}/%{realname}
Source0:	https://github.com/%{upstream}/%{realname}/archive/%{version}/%{realname}-%{version}.tar.gz
Patch1:		erlang-lfe-0001-Remove-support-for-erlang-packages.patch
%if 0%{?need_bootstrap}
BuildRequires:	erlang-erts
%else
BuildRequires:	erlang-rebar
%endif
BuildRequires:	pkgconfig


%description
Lisp Flavoured Erlang, is a lisp syntax front-end to the Erlang
compiler. Code produced with it is compatible with "normal" Erlang
code. An LFE evaluator and shell is also included.

%package -n emacs-erlang-lfe
Summary:	Emacs major mode for Lisp Flavoured Erlang
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs(bin) >= %{_emacs_version}
BuildArch:	noarch

%description -n emacs-erlang-lfe
This package provides an Emacs major mode to edit Lisp Flavoured Erlang
files.

%package -n emacs-erlang-lfe-el
Summary:	Elisp source files for Lisp Flavoured Erlang under GNU Emacs
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}
Requires:	emacs(bin) >= %{_emacs_version}
BuildArch:	noarch

%description -n emacs-erlang-lfe-el
This package contains the elisp source files for Lisp Flavoured Erlang
under GNU Emacs. You do not need to install this package to run
Lisp Flavoured Erlang. Install the emacs-erlang-lfe package to use
Lisp Flavoured Erlang with GNU Emacs.


%prep
%setup -q -n %{realname}-%{version}
%patch1 -p1 -b .no_erl_packages
iconv -f iso-8859-1 -t UTF-8  examples/core-macros.lfe > examples/core-macros.lfe.utf8
mv  -f examples/core-macros.lfe.utf8 examples/core-macros.lfe


%build
%if 0%{?need_bootstrap}
mkdir ebin
/usr/bin/erlc -o ./ebin/ src/*.erl
%else
%{rebar_compile}
%endif


%install
install -m 0755 -d %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/{bin,ebin,priv}
install -p -m 0755 -D ebin/* %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -p -m 0755 -D bin/*  %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/bin/
%if 0%{?need_bootstrap}
echo "we are going to install only bare minimum of LFE - just for rebar bootstrapping"
%else
install -p -m 0755 priv/%{realname}_drv.so %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/
%endif
install -m 0755 -d %{buildroot}/%{_bindir}
ln -s %{_libdir}/erlang/lib/%{realname}-%{version}/bin/{lfe,lfec,lfescript} %{buildroot}%{_bindir}/

%check
%if 0%{?need_bootstrap}
echo "No tests during bootstrapping"
%else
rebar eunit -v
%endif


%files
%license LICENSE
%doc README.md doc/ examples/
%{_bindir}/lfe
%{_bindir}/lfec
%{_bindir}/lfescript
%{_erllibdir}/%{realname}-%{version}



%changelog
* Tue Jul 05 2016 pterjan <pterjan> 1.0.2-3.mga6
+ Revision: 1039035
- Try fixing bootstrap...
- Try to bootstrap again

* Fri May 06 2016 neoclust <neoclust> 1.0.2-2.mga6
+ Revision: 1009764
- Rebuild post boostrap
- imported package erlang-lfe

