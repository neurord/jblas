Summary: Java bindings for BLAS
Name: jblas
Version: 1.2.2
Release: 1%{?dist}
License: BSD 3-clause
Group: Optional
URL: https://jblas.sf.net
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch

BuildRequires:  jpackage-utils

BuildRequires:  java-devel

BuildRequires:  maven

BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-release-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-surefire-provider-junit4

BuildRequires:    junit
BuildRequires:    atlas-devel

Requires:       jpackage-utils
Requires:       java
Requires:	atlas

%description
Wraps BLAS (e.g. atlas) using generated code.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%build
libdir="$(cd "/usr/lib/$(gcc -print-multi-os-directory)"; pwd)"
./configure --ptatlas --libpath="$libdir/atlas"
export LC_ALL="en_US.utf8"
make
mvn-rpmbuild package javadoc:aggregate

%install

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/jblas-1*-SNAPSHOT.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/apidocs/ $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%check
mvn-rpmbuild verify

%files
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar
%doc

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Wed Jan 30 2013 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - jblas-1
- Initial build.
