#
# TODO:
# - support for libdclassify
# - oracle driver
#
# Conditional build:
%bcond_without	mysql	# enable MySQL storage driver
%bcond_without	pgsql	# enable PostgreSQL storage driver
%bcond_without	sqlite	# enable SQLite3 storage driver
%bcond_without	db
%bcond_without	daemon

Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Summary(pl):	Biblioteka i MDA do bayesowskiego filtrowania spamu
Name:		dspam
Version:	3.6.0
Release:	0.3
License:	GPL
Group:		Applications/Mail
Source0:	http://www.nuclearelephant.com/projects/dspam/sources/%{name}-%{version}.tar.gz
# Source0-md5:	d9ee63a8cf67ea933d711b00851ce916
Source1:	%{name}.init
URL:		http://www.nuclearelephant.com/projects/dspam/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	clamav-devel
BuildRequires:	openldap-devel
%{?with_db:BuildRequires:	db-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	zlib-devel
BuildRequires:	sed >= 4.0
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

The DSPAM agent masquerades as the email server's local delivery agent
and filters/learns spams using an advanced Bayesian statistical
approach (based on Bayes's theorem of combined probabilities) which
provides an administratively maintenance-free, easy-learning Anti-Spam
service custom tailored to each individual user's behavior. Advanced
because on top of standard Bayesian filtering is also incorporated the
use of Chained Tokens, de-obfuscation, and other enhancements. DSPAM
works great with Sendmail and Exim, and should work well with any
other MTA that supports an external local delivery agent (postfix,
qmail, etc.)

%description -l pl
DSPAM (czyli De-Spam) to projekt o otwartych ¼ród³ach maj±cy na celu
stworzenie nowego rodzaju mechanizmu antyspamowego. Aktualnie jest
efektywny zarówno jako dzia³aj±cy po stronie serwera agent dla
uniksowych serwerów pocztowych jak i biblioteka dla programistów
klientów pocztowych, innych narzêdzi antyspamowych i innych projektów
wymagaj±cych filtrowania spamu w locie.

Agent DSPAM zachowuje siê jak lokalny agent dostarczania poczty (MDA)
i filtruje/uczy siê spamu przy u¿yciu zaawansowanego bayesowskiego
przybli¿enia statystycznego (opartego na twierdzeniu Bayesa o
po³±czonych prawdopodobieñstwach), daj±c nie wymagaj±c± obs³ugi
administracyjnej, ³atwo ucz±c± siê us³ugê antyspamow± dostosowan± do
zachowania ka¿dego u¿ytkownika. Metoda jest zaawansowana poniewa¿ na
podstawie standardowego filtrowania bayesowskiego wprowadzono u¿ycie
tokenów ³añcuchowych, eliminowanie ukrywanie i inne rozszerzenia.
DSPAM dzia³a wspaniale z Sendmailem i Eximem, powinien dzia³aæ dobrze
z ka¿dym innym MTA obs³uguj±cym zewnêtrznego agenta MDA (postfiksem,
qmailem itd.).

%package client
Summary:	dspam client
Summary(pl):	Klient dspam
Group:		Applications/Mail
# to get the same dspam.conf when both installed
Conflicts:	dspam > %{version}-%{release}
Conflicts:	dspam < %{version}-%{release}

%description client
dspam client.

%description client -l pl
Klient dspam.

%package libs
Summary:	A library for Bayesian spam filtering
Summary(pl):	Biblioteka do bayesowskiego filtrowania spamu
Group:		Libraries
Requires:	%{name}-driver = %{version}-%{release}

%description libs
DSPAM (as in De-Spam) is an open-source project to create a new kind
of anti-spam mechanism, and is currently effective as both a
server-side agent for UNIX email servers and a developer's library for
mail clients, other anti-spam tools, and similar projects requiring
drop-in spam filtering.

This package contains the library.

%description libs -l pl
DSPAM (czyli De-Spam) to projekt o otwartych ¼ród³ach maj±cy na celu
stworzenie nowego rodzaju mechanizmu antyspamowego. Aktualnie jest
efektywny zarówno jako dzia³aj±cy po stronie serwera agent dla
uniksowych serwerów pocztowych jak i biblioteka dla programistów
klientów pocztowych, innych narzêdzi antyspamowych i innych projektów
wymagaj±cych filtrowania spamu w locie.

Ten pakiet zawiera wspomnian± bibliotekê.

%package devel
Summary:	Header files for the DSPAM library
Summary(pl):	Pliki nag³ówkowe biblioteki DSPAM
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
DSPAM has had its core engine moved into a separate library, libdspam.
This library can be used by developers to provide 'drop-in' spam
filtering for their mail client applications, other anti-spam tools,
or similar projects.

%description devel -l pl
G³ówny silnik DSPAM zosta³ przeniesiony do oddzielnej biblioteki
libdspam, która mo¿e byæ u¿ywana przez programistów do zapewnienia
filtrowania spamu w locie dla aplikacji klientów pocztowych, innych
narzêdzi antyspamowych i podobnych projektów.

%package static
Summary:	Static DSPAM library
Summary(pl):	Statyczna biblioteka DSPAM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DSPAM library.

%description static -l pl
Statyczna biblioteka DSPAM.

%package driver-hash
Summary:	HASH driver for DSPAM
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-hash
HASH driver for DSPAM.

%package driver-db
Summary:	DB driver for DSPAM
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-db
DB driver for DSPAM.

%package driver-mysql
Summary:	MySQL driver for DSPAM
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-mysql
MySQL driver for DSPAM.

%package driver-pgsql
Summary:	PostgreSQL driver for DSPAM
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-pgsql
PostgreSQL driver for DSPAM.

%package driver-sqlite
Summary:	SQLite driver for DSPAM
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-driver = %{version}-%{release}

%description driver-sqlite
SQLite driver for DSPAM.

%prep
%setup -q
sed -i -e 's#\-static##g' src/Makefile* src/*/Makefile*

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?debug: --enable-debug --enable-bnr-debug --enable-verbose-debug} \
	--enable-trusted-user-security \
	--enable-bias \
	--enable-large-scale \
	--with-userdir=/var/lib/%{name} \
	--with-dspam-home=/var/lib/%{name} \
	--with-userdir-owner=none \
	--with-userdir-group=none \
	--with-dspam-owner=none \
	--with-dspam-group=none \
	--with-signature-life=14 \
	--disable-dependency-tracking \
	--enable-ldap \
	--enable-clamav \
	--enable-preferences-extension \
	--enable-long-usernames \
	--enable-neural-networking \
        --enable-virtual-users \
        --with-storage-driver=hash_drv%{?with_db:,libdb4_drv}%{?with_mysql:,mysql_drv}%{?with_pgsql:,pgsql_drv}%{?with_sqlite:,sqlite_drv} \
%if %{with mysql}
	--with-mysql-includes=%{_includedir}/mysql \
	--with-mysql-libraries=%{_libdir} \
%endif
%if %{with pgsql}
	--with-pgsql-includes=%{_includedir}/postgresql \
	--with-pgsql-libraries=%{_libdir} \
%endif
%if %{with sqlite}
	--with-sqlite3-includes=%{_includedir} \
	--with-sqlite3-libraries=%{_libdir} \
%endif
	--enable-daemon

# --enable-dclassify-extension needs libdclassify

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dspam

# install devel files
install -d $RPM_BUILD_ROOT{%{_includedir}/%{name},/var/lib/%{name}}
install src/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}

# provide maintenance scripts
install -d $RPM_BUILD_ROOT/etc/cron.daily
install -d $RPM_BUILD_ROOT/etc/cron.weekly

cat > $RPM_BUILD_ROOT/etc/cron.daily/%{name} <<EOF
#!/bin/sh
exec %{_bindir}/%{name}_clean -s -p
EOF

chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/%{name}

# fix prefix
sed -i -e "s|%{_prefix}/local|%{_prefix}|g" $RPM_BUILD_ROOT%{_bindir}/%{name}_corpus
sed -i -e "s|%{_prefix}/local|%{_prefix}|g" webui/cgi-bin/dspam.cgi

# fix purge stuff
#install dspam-cron.weekly $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly/%{name}

%if %{with mysql}
# fix missing file
install -d $RPM_BUILD_ROOT/var/lib/%{name}
cat > $RPM_BUILD_ROOT/var/lib/%{name}/mysql.data <<EOF
_UNCONFIGURED_

Note!

This file can only contain 5 lines with the following values:

HOSTNAME
PORT
USERNAME
PASSWORD
DATABASE
EOF
%endif

%if %{with pgsql}
# fix missing file
install -d $RPM_BUILD_ROOT/var/lib/%{name}
cat > $RPM_BUILD_ROOT/var/lib/%{name}/pgsql.data <<EOF
_UNCONFIGURED_

Note!

This file can only contain 5 lines with the following values:

HOSTNAME
PORT
USERNAME
PASSWORD
DATABASE
EOF
%endif

%post
/sbin/chkconfig --add dspam
if [ -f /var/lock/subsys/dspam ]; then
	/etc/rc.d/init.d/dspam restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/dspam start\" to start dspam daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dspam ]; then
		/etc/rc.d/init.d/dspam stop 1>&2
	fi
	/sbin/chkconfig --del dspam
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README CHANGELOG RELEASE.NOTES UPGRADING
%doc webui/*/*.{cgi,prefs,txt} webui/*/*.txt webui/*/templates/*.html
%doc doc/{courier,exim,markov,pop3filter,postfix,qmail,relay,sendmail}.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dspam.conf
%dir %attr(750,root,mail) /var/lib/%{name}
%attr(755,root,root) %config(noreplace) /etc/cron.daily/%{name}
%attr(755,root,mail) %{_bindir}/%{name}
%attr(755,root,mail) %{_bindir}/%{name}_logrotate
%attr(755,root,root) %{_bindir}/%{name}_clean
%attr(755,root,root) %{_bindir}/%{name}_corpus
%attr(755,root,root) %{_bindir}/%{name}_crc
%attr(755,root,root) %{_bindir}/%{name}_dump
%attr(755,root,root) %{_bindir}/%{name}_genaliases
%attr(755,root,root) %{_bindir}/%{name}_stats
%attr(755,root,root) %{_bindir}/%{name}_merge
%attr(755,root,root) %{_bindir}/%{name}_2sql
%attr(755,root,root) %{_bindir}/%{name}_admin
%{_mandir}/man?/%{name}*

%if %{with daemon}
%attr(754,root,root) /etc/rc.d/init.d/dspam
%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dspam.conf
%endif
%attr(755,root,mail) %{_bindir}/%{name}c

%files libs
%defattr(644,root,root,755)
%doc README CHANGELOG
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %exclude %{_libdir}/lib*_drv*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %exclude %{_libdir}/lib*_drv*.so*
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_mandir}/man3/libdspam*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files driver-hash
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/css*
%attr(755,root,root) %{_libdir}/libhash_drv*.so*

%if %{with db}
%files driver-db
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdb4_drv*.so*
%endif

%if %{with mysql}
%files driver-mysql
%defattr(644,root,root,755)
%doc doc/mysql_drv.txt src/tools.mysql_drv/*.sql
%attr(640,root,mail) %config(noreplace) /var/lib/%{name}/mysql.data
%attr(755,root,root) %{_libdir}/libmysql_drv*.so*
%endif

%if %{with pgsql}
%files driver-pgsql
%defattr(644,root,root,755)
%doc doc/pgsql_drv.txt src/tools.pgsql_drv/*.sql
%attr(640,root,mail) %config(noreplace) /var/lib/%{name}/pgsql.data
%attr(755,root,root) %{_bindir}/%{name}_pg2int8
%attr(755,root,root) %{_libdir}/libpgsql_drv*.so*
%endif

%if %{with sqlite}
%files driver-sqlite
%defattr(644,root,root,755)
%doc doc/sqlite_drv.txt
%attr(755,root,root) %{_libdir}/libsqlite_drv*.so*
%endif
