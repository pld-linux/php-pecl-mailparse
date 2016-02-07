%define		php_name	php%{?php_suffix}
%define		modname	mailparse
%define		status		stable
Summary:	%{modname} - email message manipulation
Summary(pl.UTF-8):	%{modname} - obrabianie wiadomości E-mail
Name:		%{php_name}-pecl-%{modname}
Version:	2.1.6
Release:	7
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0f84e1da1d074a4915a9bcfe2319ce84
URL:		http://pecl.php.net/package/mailparse/
BuildRequires:	%{php_name}-devel >= 4:5.2.0-7.2
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	%{php_name}-mbstring
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-mailparse < 2.1.6-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mailparse is an extension for parsing and working with email messages.
It can deal with rfc822 and rfc2045 (MIME) compliant messages.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Mailparse to rozszerzenie do analizy i pracy z wiadomościami poczty
elektronicznej. Radzi sobie z wiadomościami zgodnymi z RFC822 oraz
RFC2024 (MIME).

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure \
	--with-%{modname}=%{_prefix}/X11R6/include/X11/

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I%{_prefix}/X11R6/include/X11"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
