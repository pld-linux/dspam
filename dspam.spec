#
# Conditional build:
%bcond_with	mysql	# enable mysql storage driver (disable db4 driver)
#
Summary:	A library and Mail Delivery Agent for Bayesian spam filtering
Summary(pl):	Biblioteka i MDA do bayesowskiego filtrowania spamu
Name:		dspam
Version:	2.10.6
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://www.nuclearelephant.com/projects/dspam/sources/%{name}-%{version}.tar.gz
# Source0-md5:	ddb40d26cc923d7569d48b3072e61715
URL:		http://www.nuclearelephant.com/projects/dspam/
%if %{with mysql}
BuildRequires:	mysql-static
%else
BuildRequires:	db-static
%endif
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

%package libs
Summary:	A library for Bayesian spam filtering
Summary(pl):	Biblioteka do bayesowskiego filtrowania spamu
Group:		Libraries

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

%prep
%setup -q

%build
%configure \
	--enable-static=yes \
	--enable-trusted-user-security \
	--enable-bayesian-dobly \
	--enable-chained-tokens \
	--enable-neural-networking \
	--enable-experimental \
	--enable-signature-attachments \
	--enable-bias \
	--enable-large-scale \
	--enable-delivery-to-stdout \
	--enable-virtual-users \
	--with-userdir=/var/lib/%{name} \
	--with-userdir-owner=none \
	--with-userdir-group=none \
	--with-dspam-owner=none \
	--with-dspam-group=none \
	--with-signature-life=14 \
	--disable-dependency-tracking \
%if %{with mysql}
	--with-storage-driver=mysql_drv \
	--enable-virtual-users \
	--with-mysql-includes=%{_includedir}/mysql \
	--with-mysql-libraries=%{_libdir}
%else
	--with-storage-driver=libdb4_drv \
	--with-db4-includes=%{_includedir} \
	--with-db4-libraries=%{_libdir}
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

#%makeinstall_std
%{__make} install DESTDIR=$RPM_BUILD_ROOT

# install devel files
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install -m0644 libdspam.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -m0644 libdspam_objects.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -m0644 lht.h $RPM_BUILD_ROOT%{_includedir}/%{name}
install -m0644 nodetree.h $RPM_BUILD_ROOT%{_includedir}/%{name}

# provide maintenance scripts
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly

cat > $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/%{name} <<EOF
#!/bin/sh
exec %{_bindir}/%{name}_clean 2>&1 > /dev/null
EOF

chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/%{name}

# fix prefix
perl -pi -e "s|%{_prefix}/local|%{_prefix}|g" $RPM_BUILD_ROOT%{_bindir}/%{name}_corpus
perl -pi -e "s|%{_prefix}/local|%{_prefix}|g" cgi/dspam.cgi

cp tools.mysql_drv/README README.mysql

# fix purge stuff
install -m0755 dspam-cron.weekly $RPM_BUILD_ROOT%{_sysconfdir}/cron.weekly/%{name}

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README CHANGE
%doc cgi/base.css cgi/dspam.cgi cgi/logo.gif cgi/template.html
%doc README.mysql
%doc tools.mysql_drv/mysql_objects.sql.space.optimized
%doc tools.mysql_drv/mysql_objects.sql.speed.optimized
%doc tools.mysql_drv/purge.sql
%doc tools.mysql_drv/virtual_users.sql
%dir %attr(0750,root,mail) /var/lib/%{name}
%attr(640,root,mail) %config(noreplace) /var/lib/%{name}/mysql.data
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/cron.weekly/%{name}
%attr(755,root,mail) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}_clean
%attr(755,root,root) %{_bindir}/%{name}_corpus
%attr(755,root,root) %{_bindir}/%{name}_crc
%attr(755,root,root) %{_bindir}/%{name}_dump
%attr(755,root,root) %{_bindir}/%{name}_genaliases
%attr(755,root,root) %{_bindir}/%{name}_stats
%attr(755,root,root) %{_bindir}/%{name}_merge
%attr(755,root,root) %{_bindir}/%{name}_2mysql
%attr(755,root,root) %{_bindir}/%{name}_ngstats

%files libs
%defattr(644,root,root,755)
%doc README CHANGE
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
